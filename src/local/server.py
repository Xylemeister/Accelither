import threading
import random
import pygame
from netcode.TCPConnection import TCPConnection
import json
import time
import math

#select a server port
HOST = '172.31.47.170'
PORT = 12000

ARENA_X = 1000
ARENA_Y = 1000
SCREEN_X= 720
SCREEN_Y=480
INIT_X = 500
INIT_Y = 500
FOOD_RAD = 10
SNAKE_RAD = 10
HEAD_RAD = 15

pygame.init()
clock = pygame.time.Clock()

def check_collision_circle(circle1, circle2):
    diffx = circle1[0] - circle2[0]
    diffy = circle1[1] - circle2[1]
    dist = math.sqrt(diffx**2 + diffy**2)
    if dist < circle1[2] + circle2[2]:
        return True
    else:
        return False
    
def check_collision_circle_list(circle, circle_list):
    for c in circle_list:
        if check_collision_circle(circle,c):
            return True
    return False

class Player:
    def __init__(self, player_id, x, y):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.body = [(x,y) for _ in range(0,10)]
        self.score = 0
        self.dirX = 0
        self.dirY = 0
        self.speed = 5

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "body": [(round(x,2),round(y,2)) for (x,y) in self.body],
            "score": self.score,
            "dirX" : round(self.dirX, 2),
            "dirY" : round(self.dirY, 2)
        }

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            "x": round(self.x, 2),
            "y": round(self.y, 2)
        }

class GameData:
    def __init__(self):
        self.players = {}
        self.foods = [Food(random.randint(FOOD_RAD, ARENA_X - FOOD_RAD), random.randint(FOOD_RAD, ARENA_Y - FOOD_RAD)) for _ in range(0,10)]
        self.lock = threading.Lock()

    def add_player(self, player_id):
        print("added player")
        with self.lock:
            not_valid = True
            x,y = 0,0
            while not_valid:
                not_valid = False
                x = random.randint(100, ARENA_X-100)
                y = random.randint(100, ARENA_Y-100)
                for player in self.players.values():
                    dist = math.sqrt((player.x-x)**2 + (player.y-y)**2)
                    if dist < 200:
                        not_valid = True
                        break
            self.players[player_id] = Player(player_id, x, y)

    def remove_player(self, player_id):
        with self.lock:
            if player_id in self.players:
                del self.players[player_id]

    def set_player_speed(self, player_id, speed):
        with self.lock:
            self.players[player_id].speed = speed

    def move_player(self, player_id, x_in, y_in):
        with self.lock:
            if player_id in self.players:
                player = self.players[player_id]
                # Calculate the magnitude of the vector
                magnitude = math.sqrt(x_in**2 + y_in**2)
    
                # Normalize the vector
                if magnitude != 0:
                    x_in /= magnitude
                    y_in /= magnitude
                    player.dirX = x_in
                    player.dirY = y_in
                    
                else: 
                    x_in = player.dirX
                    y_in = player.dirY

                player.x -= x_in * player.speed
                player.y += y_in * player.speed
                player.body.insert(0, (player.x, player.y))
    
    def reduce_player_body(self, player_id):
        with self.lock:
            if player_id in self.players:
                self.players[player_id].body.pop()

    def generate_food(self):
        with self.lock:
            x = random.randint(FOOD_RAD, ARENA_X - FOOD_RAD)
            y = random.randint(FOOD_RAD, ARENA_Y - FOOD_RAD)
            self.foods.append(Food(x, y))

    def check_collision_player(self, player_id) -> bool:
        player = self.players[player_id]
        player_head_circle = (player.x, player.y,SNAKE_RAD)
        
        all_player_bodies = []
        for other_player in self.players.values():
            if other_player.player_id != player_id:
                for index, segment in enumerate(other_player.body):
                    if index == 0:
                        all_player_bodies.append((segment[0],segment[1],HEAD_RAD))
                    else:
                        all_player_bodies.append((segment[0],segment[1],SNAKE_RAD))
        if check_collision_circle_list(player_head_circle, all_player_bodies):
            print("player colision " + str(player_id))
            return True
        if (player.x < SNAKE_RAD or player.x > ARENA_X-SNAKE_RAD or player.y < SNAKE_RAD or player.y > ARENA_Y-SNAKE_RAD):
            print("wall collision " + str(player_id))
            return True
        return False
    
    def render_to_player(self, player_id):
        centerx = self.players[player_id].x
        centery = self.players[player_id].y
        return_dict = self.to_dict()
        for player in return_dict['players']:
            player['x'] = round(player['x'] - centerx+SCREEN_X//2,1)
            player['y'] = round(player['y'] - centery+SCREEN_Y//2,1)
            player['body'] = [(round(x-centerx+SCREEN_X//2,1), round(y-centery+SCREEN_Y//2,1)) for x,y in player['body']]

        for food in return_dict['foods']:
            food['x'] = round(food['x'] - centerx+SCREEN_X//2,1)
            food['y'] = round(food['y'] - centery+SCREEN_Y//2,1)
        return return_dict, (round(SCREEN_X//2-centerx,1), round(SCREEN_Y//2-centery,1))

    
    def check_eat_food(self, player_id):
        player = self.players[player_id]
        player_head_circle = (player.x,player.y,SNAKE_RAD)
        food_circles = [(food.x, food.y, FOOD_RAD) for food in self.foods]
        for index, food_circle in enumerate(food_circles):
            if check_collision_circle(player_head_circle,food_circle):
                with self.lock:
                    self.foods.pop(index)
                    player.score += 1
                self.generate_food()
                return True
        self.reduce_player_body(player_id)
        return False


    def to_dict(self):
        return {
            "players": [player.to_dict() for player in self.players.values()],
            "foods": [food.to_dict() for food in self.foods]
        }

class ServerThread(threading.Thread):
    def __init__(self, connection: TCPConnection, player_id: int, game_data: GameData):
        super().__init__()
        self.connection = connection
        self.game_data = game_data
        self.player_id = player_id
        self.alive = True
        self.game_data.add_player(player_id)

    def run(self):
        while self.connection.isAlive(self.player_id):
            if not self.alive:
                time.sleep(0.1)
                print("remove player")
                self.game_data.remove_player(self.player_id)
            client_input = self.connection.recv(self.player_id)
            # this kills player via TCPConnection
            if client_input:
                json_msg = client_input.decode()
                msg = json.loads(json_msg)
                x = msg["x"]
                y = msg["y"]
                speed = msg["speed"]
                self.game_data.set_player_speed(self.player_id, speed)
                self.game_data.move_player(self.player_id, x, y)
                eaten = self.game_data.check_eat_food(self.player_id)
                collide = self.game_data.check_collision_player(self.player_id)
                if collide:
                    self.alive = False
                game_state, boundary_box = self.game_data.render_to_player(self.player_id)
                game_state['alive'] = self.alive
                game_state['score'] = self.game_data.players[self.player_id].score
                game_state['food_eaten'] = eaten
                game_state['boundary_box'] = boundary_box
                msg = json.dumps(game_state)
                self.connection.send(msg.encode(), self.player_id)
                print("sent")
        

def main():

    game_data = GameData()

    server = TCPConnection(HOST, PORT, host=True)
    server.setMaxClients(5)

    while server.isAlive():
        client_index = server.acceptNewClient()
        if client_index is not None:
            server_thread = ServerThread(server, client_index, game_data)
            server_thread.start()
        #print(game_data.to_dict())
        clock.tick(60)

if __name__ == "__main__":
    main()
