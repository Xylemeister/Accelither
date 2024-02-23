# Game Design Document (GDD) 

**Game will probably adapted from an existing implementation**

**This page is an intial template to expand**

## 1. Game Concept
- **Title**: slither_FPGA
- **Concept**: slither controlled through a DE10 lite fpga with possible extra functionality enabled through this

## 2. Gameplay
- **Objective**:
  - Grow as large as possible
  - Stay at the top of the leaderboard as long as possible
  - Eliminate as many players as posible
- **Mechanics**:
  - Snake moving in 2d game plane
  - Snake can accelerate
  - If a snake hits another snakes body it dies
  - Snakes could possibly pick up and activate special abilities
- **Controls**:
  - Polar coordinates recieved from accelerometer for control in the 2d game plane
  - Possibly jerk up and down in z axis to activate ability etc reading rapid change in z values
  - Hold down button to accelerate
  - further functionality ....
- **Level**:
  -  Single level with defined game arena due to limited player count
  -  Could have a wraparound game plane, would be quite impressive, possibly quite complex

## 3. Story and Setting
- **Narrative**:
  - Could make a story for the snakes.
- **World**:
  - Level design could try and mimik a simplified biome with obstacles in the plane
 

## 4. Art and Aesthetics
- **Visual Style**:
  - Visual theme could tie in with story of the snakes
- **Characters**:
  - Simple 2d art of snakes
  - Could have multiple presets to choose, or randomly start with one (not really needed). 
- **UI/UX Design**:
  - Very minimal and small
  - Small box in a corner to display current held ability
  - Current score
  - Current position in the size leaderboard
  - Number of enimies killed
  - Survival time

## 5. Sound and Music
- **Sound Effects**:
  - Sound played through laptop when you die or kill an enemy
  - Achievement sound when you become top of the leaderboard
  - Maybe have sound that plays when you make it pass a certain score or time e.g your highscore in size and survival time. Or other significant intervals
- **Music**:
  - Not really needed, could have simple tune if we really wanted to

## 6. Multiplayer
- **Network Play**:
  - Competitive survival, can eliminate other players
- **Server Architecture**: (Need to figure out)
  - Will we go straight from fpga to game input or through the sever first?
  - P2P or client-server?
  - How will we connect and interact?
- **Matchmaking and Lobbies**:
  - How do we join a game instance?
  - Is there one concurrent room?  

## 7. Technology
- **Engine**:
  - Probaby won't use one
- **Platforms**:
  - Strictly downloadable executable or web app?
- **FPGA Integration**: 
  -  How will the FPGA's data be integrated into the game?
  -  Need to detail the data flow and processing. 

## 8. Development and Production
- **Timeline**:
  - Put major milestones here, possibly have a timeline in another software or formate e.g gantt chart **To edit**
- **Team Roles**:
  -  We need to list team members and their roles/responsibilities. Also possibly through another format. Could have a work sprint **To edit**

## 9. Ideas
  - Put any ideas here


**We should probably start working together, creating a timeline and assigning clear roles as soon as possible.**
