# BOVID-19
Built entirely during a ~9 hour hackathon; functional, but could use a lot of work; probably no future commits

**WARNING: The below description was quickly and sloppily made for the hackathon.**

## Description
### Inspiration
This game is inspired by the current COVID-19 pandemic and aims to spread awareness of the humanitarian benefits of doing something as simple as staying home when possible and wearing masks when not.
What it does

The objective is to prevent high risk people from getting infected by COVID-19 at all costs. One instantly loses the game if that happens.

The game begins with one COVID-19 infected person (purple square), two low risk people (green squares), and a high risk person (red square). If the infected person touches anyone else, they also get infected. If a high risk person gets infected, the game ends.

The rounds get progressively harder by adding one additional person each round in the following pattern: low risk, low risk, infected, high risk. To win a round, one must last 30 seconds without infecting the high risk person(s). The round and timer are displayed at the bottom of the screen.

Collisions between people can be avoided by building walls that expand using left click. A wall stops building on impact of another wall or person. By default, walls builds vertically, but right clicking can toggle it to build horizontally. Only one wall can be built at a time. If a person collides with a wall built by the player, it will bounce off and the wall will disintegrate and disappear.

Power ups randomly appear throughout the map and are applied to the first person to touch them. There are currently two power ups:

- The mask power up (white square) shields both the wearer and collider from spreading COVID-19. However, the mask only provides temporary protection; it disappears on collision involving an infected person. The person who picks up this power up displays a white outline.
- The quarantine power up (black square), the stronger of the two power ups, builds a "home" (four walls) around a person for the remainder of the level.

### How I built it
I used the Pygame library in Python to create this game.

For collisions, I assume ideal physics (no friction, gravity, etc. so constant velocity) and essentially follows the law where the angle an object hits is the angle it bounces off (Snell's law??).

### Challenges I ran into
In general, balancing the game was challenging; I had to tweak parameters to ensure fun game play and medium difficulty.

Specifically, having the wall continue building after colliding with a wall on one end was challenging. I tried everything from building two separate walls to having two different velocities. All attempts I made introduced new bugs, so I had to scrap it.

### Accomplishments that I'm proud of
I was able to build a functioning product in my first hackathon!

### What I learned
I recently took an online game design class at the MIT ESP HSSP summer program. I was able to apply what I learned in that class in this hackathon. I was also able to get more familiar with the Pygame library.

### What's next for Bovid 2020
I plan to add more depth to the game, including adding more power ups, and tweaking the game logic.

### Built With
- Pygame
- Python 3

### Try it out
[repl.it](https://repl.it/@abdnegm/BOVID-19)
