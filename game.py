import random
import pygame
pygame.init()

class State:
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"

    INFECTED = "Infected"
    LOW = "LOW"
    HIGH = "HIGH"

    MASK = "Mask"
    WALL = "Wall"

    ONGOING = "Ongoing"
    WON = "Won"
    LOST = "Lost"

class Color:
    BACKGROUND = (128, 128, 128) #gray
    WALL = (50, 50, 50) # blackish
    
    INFECTED = (128,0,128) #purple
    LOW = (0, 128, 0) #green
    HIGH = (255, 0, 0) #red
    MASK = (255, 255, 255) #white
    WALL_POWER = (0, 0, 0) #white
    TEXT = (255, 255, 255) #white

class Rectangle:
    def __init__(self, x, y, w, h, v_x, v_y, breakable, color, state):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v_x = v_x
        self.v_y = v_y
        self.breakable = breakable
        self.color = color
        self.state = state
    def intersects(self, other):
        if self.x >= other.x + other.w:
            return False
        if self.x + self.w <= other.x:
            return False
        if self.y >= other.y + other.h:
            return False
        if self.y + self.h <= other.y:
            return False
        return True

class Timer:
    clock = pygame.time.Clock()
    counter = 10
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, 1000)
    clock.tick(60)
    

class Game:
    def __init__(self, num_infected, num_low, num_high, num_mask, num_wall, round_num):
        self.num_infected = num_infected
        self.num_low = num_low
        self.num_high = num_high
        self.num_mask = num_mask
        self.num_wall = num_wall
        self.round_num = round_num
        
    def main(self):
        num_rows = 15
        num_cols = 23
        tile_size = 40
        length = tile_size*num_cols
        width = tile_size*num_rows

        win = pygame.display.set_mode((length, width))
        pygame.display.set_caption("BOVID-19")
        win.fill(Color.BACKGROUND)

        clock = pygame.time.Clock()
        counter = 30
        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)
        clock.tick(60)

        game_state = State.ONGOING

        direction = State.VERTICAL

        partial_wall = 0

        walls = []
        wall_speed = 5

        top_wall = Rectangle(0, 0, length, tile_size, 0, 0, False, Color.WALL, State.HORIZONTAL)
        walls.append(top_wall)
        bot_wall = Rectangle(0, width-tile_size, length, tile_size, 0, 0, False, Color.WALL, State.HORIZONTAL)
        walls.append(bot_wall)
        left_wall = Rectangle(0, 0, tile_size, width, 0, 0, False, Color.WALL, State.VERTICAL)
        walls.append(left_wall)
        right_wall = Rectangle(length-tile_size, 0, length, width, 0, 0, False, Color.WALL, State.VERTICAL)
        walls.append(right_wall)

        balls = []
        ball_size = 25
        ball_speed = 3
        for i in range(self.num_infected):
            infected = Rectangle(random.randint(tile_size, length-2*tile_size), random.randint(tile_size, width-2*tile_size), ball_size, ball_size, ball_speed, ball_speed, False, Color.INFECTED, State.INFECTED)
            balls.append(infected)
        for i in range(self.num_low):
            low = Rectangle(random.randint(tile_size, length-2*tile_size), random.randint(tile_size, width-2*tile_size), ball_size, ball_size, -ball_speed, -ball_speed, False, Color.LOW, State.LOW)
            balls.append(low)
        for i in range(self.num_high):
            high = Rectangle(random.randint(tile_size, length-2*tile_size), random.randint(tile_size, width-2*tile_size), ball_size, ball_size, ball_speed, ball_speed, False, Color.HIGH, State.HIGH)
            balls.append(high)

        powers = []
        power_size = ball_size
        for i in range(self.num_mask):
            mask = Rectangle(random.randint(tile_size, length-2*tile_size), random.randint(tile_size, width-2*tile_size), power_size, power_size, 0, 0, False, Color.MASK, State.MASK)
            powers.append(mask)
        for i in range(self.num_wall):
            wall = Rectangle(random.randint(tile_size, length-2*tile_size), random.randint(tile_size, width-2*tile_size), power_size, power_size, 0, 0, False, Color.WALL_POWER, State.WALL)
            powers.append(wall)

        masks = {}
        
        FPS = 60
        pygame.time.set_timer(pygame.USEREVENT, 1000//FPS)

        touching_mask = []

        run = True
        while run:
            if pygame.event.get(pygame.USEREVENT): # checks for events
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP: # if click event
                        if event.button == 1 and partial_wall == 0: # if left click
                            pos = pygame.mouse.get_pos()
                            if direction == State.VERTICAL:
                                wall = Rectangle(int(pos[0]-pos[0]%tile_size), int(pos[1]-pos[1]%tile_size), tile_size, 0, 0, -wall_speed, True, Color.WALL, direction)
                                overlap = False
                                for i in walls:
                                    if wall.intersects(i):
                                        overlap = True
                                        break
                                if not overlap:
                                    partial_wall = wall
                            else: 
                                wall = Rectangle(int(pos[0]-pos[0]%tile_size), int(pos[1]-pos[1]%tile_size), 0, tile_size, -wall_speed, 0, True, Color.WALL, direction)
                                overlap = False
                                for i in walls:
                                    if wall.intersects(i):
                                        overlap = True
                                        break
                                if not overlap:
                                    partial_wall = wall
                        if event.button == 3: # if right click
                            if direction == State.VERTICAL:
                                direction = State.HORIZONTAL
                            else:
                                direction = State.VERTICAL
                    if event.type == timer_event:
                        counter -= 1
                        if counter == 0:
                            pygame.time.set_timer(timer_event, 0)
                    
                    if event.type == pygame.QUIT:
                        run = False
                        return False

                win.fill(Color.BACKGROUND)

                break_mask_list = []
                for i in walls: # draws walls
                    pygame.draw.rect(win, i.color, (i.x, i.y, i.w, i.h))
                    for j in balls: # checks if walls touch balls
                        if j.intersects(i): 
                            if i.state == State.VERTICAL:
                                j.v_x *= -1
                            else:
                                j.v_y *= -1
                            if i.breakable and i in walls:
                                walls.remove(i)

                        for key in list(masks):
                            if j.intersects(key) and j != key and (j.state == State.INFECTED or key.state == State.INFECTED):
                                touching_mask.append([key,j])
                                del masks[key]
                        
                        for k in balls: # checks if balls touch balls
                            if j.intersects(k) and j != k:
                                colliding = False
                                for touching in touching_mask:
                                    if (k.state != State.INFECTED or j.state != State.INFECTED) and k in touching and j in touching and touching[0].intersects(touching[1]):
                                        colliding = True
                                    else:
                                        touching_mask.remove(touching)
                                if not colliding and j.state == State.INFECTED and (j not in masks and k not in masks):
                                    if k.state == State.HIGH:
                                        game_state = State.LOST
                                    k.state = State.INFECTED
                                    k.color = Color.INFECTED
                                
                        for k in powers: # checks if balls touch powers
                            if j.intersects(k):
                                if k.state == State.MASK:
                                    masks[j] = []
                                    top_mask = Rectangle(j.x, j.y, j.w, 0, j.v_x, j.v_y, True, Color.MASK, State.HORIZONTAL)
                                    masks[j].append(top_mask)
                                    bot_mask = Rectangle(j.x, j.y+j.h, j.w, 0, j.v_x, j.v_y, True, Color.MASK, State.HORIZONTAL)
                                    masks[j].append(bot_mask)
                                    left_mask = Rectangle(j.x, j.y, 0, j.h, j.v_x, j.v_y, True, Color.MASK, State.VERTICAL)
                                    masks[j].append(left_mask)
                                    right_mask = Rectangle(j.x+j.w, j.y, 0, j.h, j.v_x, j.v_y, True, Color.MASK, State.VERTICAL)
                                    masks[j].append(right_mask)
                                    powers.remove(k)
                                elif k.state == State.WALL:
                                    if j.state == State.INFECTED and self.round_num < 4:
                                        counter = 3
                                    if j.state == State.HIGH and self.round_num < 5:
                                        counter = 3
                                    j.v_x = 0
                                    j.v_y = 0
                                    top_w = Rectangle(j.x-tile_size/2, j.y-tile_size/2, j.w+tile_size, tile_size/2, j.v_x, j.v_y, False, Color.WALL, State.HORIZONTAL)
                                    walls.append(top_w)
                                    bot_w = Rectangle(j.x-tile_size/2, j.y+j.h, j.w+tile_size, tile_size/2, j.v_x, j.v_y, False, Color.WALL, State.HORIZONTAL)
                                    walls.append(bot_w)
                                    left_w = Rectangle(j.x-tile_size/2, j.y-tile_size/2, tile_size/2, j.h+tile_size, j.v_x, j.v_y, False, Color.WALL, State.VERTICAL)
                                    walls.append(left_w)
                                    right_w = Rectangle(j.x+j.w, j.y, tile_size/2, j.h+tile_size/2, j.v_x, j.v_y, False, Color.WALL, State.VERTICAL)
                                    walls.append(right_w)
                                    powers.remove(k)
                            
                for i in powers:
                    pygame.draw.rect(win, i.color, (i.x, i.y, i.w, i.h))

                for i in balls: #draws balls
                    i.x += i.v_x
                    i.y += i.v_y
                    pygame.draw.rect(win, i.color, (i.x, i.y, i.w, i.h))
                    if i in masks: # draws mask around balls
                        for j in masks[i]:
                            j.x += i.v_x
                            j.y += i.v_y
                            pygame.draw.rect(win, j.color, (j.x, j.y, j.w, j.h))
                
                if partial_wall != 0:
                    for i in walls:
                        if partial_wall.intersects(i): #checks if partial walls touch walls
                            walls.append(partial_wall)
                            partial_wall = 0
                            break
                    if partial_wall != 0: #checks if partial walls touch balls
                        for i in balls:
                            if partial_wall.intersects(i):
                                if partial_wall.state == State.VERTICAL:
                                    i.v_x *= -1
                                else:
                                    i.v_y *= -1
                                partial_wall = 0
                                break
                        if partial_wall != 0: #draws partial walls
                            wall.x += wall.v_x
                            wall.y += wall.v_y
                            wall.w -= 2*wall.v_x
                            wall.h -= 2*wall.v_y
                            pygame.draw.rect(win, partial_wall.color, (partial_wall.x, partial_wall.y, partial_wall.w, partial_wall.h))

                font = pygame.font.SysFont(None, 24)
                time_text = font.render("Round: " + str(self.round_num), True, Color.TEXT)
                win.blit(time_text, (tile_size, width-tile_size/2))
                time_text = font.render("Time Left: " + str(counter) + " seconds", True, Color.TEXT)
                win.blit(time_text, (tile_size*4, width-tile_size/2))

                if counter == 0:
                    game_state = State.WON
                    run = False
                    return True
                elif game_state == State.LOST:
                    run = False
                    return
                pygame.display.update()

round_num = 1
num_infected = 1
num_low = 2
num_high = 1
num_mask = 1
num_wall = 0

while True:
    if round_num % 5 == 0:
        num_high += 1
    elif round_num % 4 == 0:
        num_infected += 1
    elif round_num != 1:
        num_low += 1
    if round_num == 2:
        num_wall = 1
        
    game = Game(num_infected, num_low, num_high, num_mask, num_wall, round_num)
    main = game.main()
    
    if main == False:
        break
    elif main == True:
        round_num += 1
    else:
        round_num = 1
        num_infected = 1
        num_low = 2
        num_high = 1
pygame.quit()
