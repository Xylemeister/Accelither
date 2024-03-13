import pygame
import json
import de10 as acc
from netcode.TCPConnection import TCPConnection
import time
import math
import game_pb2

# Server IP address and port
HOST = '18.130.236.221'
PORT = 12000

# Screen dimensions
SCREEN_X = 720
SCREEN_Y = 480

# Snake and food dimensions
SCORE_COLOUR = (255, 0, 247)
FOOD_RAD = 10
SNAKE_RAD = 10
HEAD_RAD = 15
BASE_SPEED = 3

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('Snake Game Client')

sounds = { "omnom" : pygame.mixer.Sound("eat_sound.mp3"),
           "oopsydaisy" : pygame.mixer.Sound("collision_sound.mp3"),
           "womp_womp" : pygame.mixer.Sound("womp-womp.mp3")
         }

import pygame
import sys

def protobuf_to_dict(protobuf_message):
    result = {
        "players": [],
        "foods": [],
        "alive": protobuf_message.alive,
        "score": protobuf_message.score,
        "food_eaten": protobuf_message.food_eaten,
        "boundary_box": tuple(protobuf_message.boundary_box),
    }
    
    # Convert players
    for player in protobuf_message.players:
        player_data = {
            "player_id": player.player_id,
            "username": player.username,
            "x": player.position.x,
            "y": player.position.y,
            "score": player.score,
            "dirX": player.dirX,
            "dirY": player.dirY,
            "body": [(coord.x, coord.y) for coord in player.body],
        }
        result["players"].append(player_data)
    
    # Convert foods
    for food in protobuf_message.foods:
        food_data = {"x": food.position.x, "y": food.position.y}
        result["foods"].append(food_data)
    
    return result


def input_username():

    # Set up fonts
    font = pygame.font.SysFont(None, 32)

    username = ""
    input_rect = pygame.Rect(100, 100, 200, 50)
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)

        text_surface = font.render(username, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

def get_angle(x, y):
    
    # Calculate the angle using arctangent (in radians) and convert to degrees
    angle_rad = math.atan2(y, x)  # Note the negative sign for y
    angle_deg = math.degrees(angle_rad)

    return angle_deg-90


def show_score(choice, colour, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, colour)
    score_rect = score_surface.get_rect()
    acc.Input.set7Seg(0,(0,0,0,0,0,0,0))
    acc.Input.set7Seg(1,(0,0,0,0,0,0,0))
    acc.Input.set7Seg(2,(0,0,0,0,0,0,0))
    acc.Input.set7Seg(3,(0,0,0,0,0,0,0))
    acc.Input.set7Seg(4,str(score//10))
    acc.Input.set7Seg(5,str(score%10))
    if choice == 1:
        score_rect.midtop = (SCREEN_X/10, 15)
    else:
        score_rect.midtop = (SCREEN_X/2, SCREEN_Y/1.25)
    screen.blit(score_surface, score_rect)

def gamover(score, connection):
    print("enter gameover")
    sounds["oopsydaisy"].play()
    my_font = pygame.font.SysFont('Times New Roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, (252,3,3) )
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_X/2, SCREEN_Y/4)
    screen.fill((10,10,10))
    screen.blit(game_over_surface, game_over_rect)
    show_score(0, (252,3,3), 'Comic Sans', 20, score)

    # Display leaderboard data
    font = pygame.font.SysFont('Times New Roman', 32)
    y_offset = SCREEN_Y/2

    leaderboard_data_json = {}
    not_valid = True
    while not_valid:
        try: 
            leaderboard_data = connection.recv(timeout=0.5)
            leaderboard_data_json = json.loads(leaderboard_data.decode())
            print(leaderboard_data_json[0]['HighScore'])
            not_valid = False
        except:
            continue

    for rank, score_dict in enumerate(leaderboard_data_json, start=1):
        rank_text = font.render(str(rank), True, (252,3,3))
        screen.blit(rank_text, (50, y_offset))
        username_text = font.render(score_dict['PlayerId'], True, (252,3,3))
        screen.blit(username_text, (100, y_offset))
        score_text = font.render(str(score_dict['HighScore']), True, (252,3,3))
        screen.blit(score_text, (300, y_offset))
        y_offset += 30    

    pygame.display.flip()
    sounds["womp_womp"].play()
    time.sleep(5)
    pygame.quit()

def blitRotate(surf, image, origin, pivot, angle):
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotozoom(image, angle, 0.7)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

# Function to render game state
def render_game_state(screen, game_state):
    # Clear the screen
    screen.fill((0, 0, 0))
    snake_head = pygame.image.load('snake.svg')
    
    for player_data in game_state['players']:
        username = player_data['username']
        dirX = player_data['dirX']
        dirY = player_data['dirY']
        for index, segment in enumerate(reversed(player_data['body'])):
            if index == len(player_data['body'])-1:  # Draw the head of the snake
                blitRotate(screen, snake_head, segment, (21.3,20), get_angle(dirX,dirY))
            else:
                pygame.draw.circle(screen, (160, 196, 50), segment, SNAKE_RAD)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(username, True, (255, 255, 255))
        headx = player_data['body'][0][0]
        heady = player_data['body'][0][1]
        text_rect = text_surface.get_rect(center=(headx, heady-30))
        screen.blit(text_surface,text_rect)
    
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(game_state['boundary_box'][0], game_state['boundary_box'][1], 1000, 1000), 3)

    if (game_state['food_eaten']):
        sounds['omnom'].play()

    # Render food
    foods = game_state['foods']
    for food in foods:
        pygame.draw.circle(screen, (255, 0, 0), (food['x'], food['y']), FOOD_RAD)
    show_score(1, SCORE_COLOUR, 'Comic Sans', 20, game_state['score'])

    # Update the display
    pygame.display.flip()

# Main function to run the client
def main():
    username = input_username()
    # Initialize the TCP connection
    connection = TCPConnection(HOST, PORT)

    not_break = True
    
    msg_init = {
        'username' : username,
        'x' : acc.Input.getX(),
        'y' : acc.Input.getY(),
        'speed': BASE_SPEED+acc.Input.getButton(0)*2-acc.Input.getButton(1)*2}

    msg_json_init = json.dumps(msg_init)
        
    #send the message to the udp server
    connection.send(msg_json_init.encode())
    time.sleep(0.02)
    
    # Main loop
    while not_break:
        msg = {
        'username' : username,
        'x' : acc.Input.getX(),
        'y' : acc.Input.getY(),
        'speed': BASE_SPEED+acc.Input.getButton(0)*2-acc.Input.getButton(1)*2}

        msg_json = json.dumps(msg)
        
        #send the message to the udp server
        connection.send(msg_json.encode())

        # Receive game state from the server
        
        game_state_json = connection.recv(timeout=0.1)
        received_game_data = game_pb2.GameData()
        received_game_data.ParseFromString(game_state_json)
        '''
        curr = 0
        for ind,char in enumerate(game_state_json):
            if char == '{':
                curr+=1
            elif char == '}':
                curr-=1
            if curr == 0:
                game_state_json = game_state_json[:ind+1]
        '''
        if received_game_data:
            try:
                #game_state = json.loads(game_state_json)
                game_state = protobuf_to_dict(received_game_data)
                score = game_state['score']
                render_game_state(screen, game_state)
                if not game_state['alive']:
                    gamover(score, connection)
                    connection.close()
                    sys.exit()
            except:
                print(game_state_json)
                continue
        # Tick the clock
        clock.tick(60)

if __name__ == "__main__":
    main()
    sys.exit()
