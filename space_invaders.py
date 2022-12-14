import pygame
import random
import math
from pygame import mixer

# creating our first window
# whenever you want to create a game ,write this line otherwise it will not work ie initialize the pygame

pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 800))
# background = pygame.image.load('background.jpg')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1) 


# Title, icon
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Invaders')

# Player
Player_IMG = pygame.image.load('aircraft.png')
Player_x_axis = 370
Player_y_axis = 620
Player_x_y_change = 0


# Enemy
Enemy_IMG = []
Enemy_x_axis = []
Enemy_y_axis = []
Enemy_x_change = []
Enemy_y_change = []

num_of_enemies = 15
for i in range(num_of_enemies):
    Enemy_IMG.append(pygame.image.load('enemy.png'))
    Enemy_x_axis.append(random.randint(0, 736))
    Enemy_y_axis.append(random.randint(40, 250))
    Enemy_x_change.append(0.1)
    Enemy_y_change.append(38)

# bullets
# Fire - the bullet is currently moving 
Bullet_IMG = pygame.image.load('bullets.png')
Bullet_x_axis = 0
Bullet_y_axis = 620
Bullet_x_change = 0
Bullet_y_change = 0.8
bullet_state = "ready" # you cant see the bullet on the screen

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
txt_x = 10
txt_y = 10




# gameover
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 350))

def player(x, y):
    screen.blit(Player_IMG, (x, y))  # blit means draw
    # now call this func in running loop becoz we dont want it to get disappear from window

def enemy(x, y, i):
    screen.blit(Enemy_IMG[i], (x, y))  # blit means draw
    # now call this func in running loop becoz we dont want it to get disappear from window

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(Bullet_IMG, (x+16, y+10))


def is_collision(Enemy_x_axis, Enemy_y_axis, Bullet_x_axis, Bullet_y_axis):
    distance = math.sqrt((math.pow(Enemy_x_axis - Bullet_x_axis,2)) + (math.pow(Enemy_y_axis - Bullet_y_axis, 2)))
    if distance < 27:
        return True
    return False


# game loop
running = True
while running:
    # Background rgb
    screen.fill((0, 0, 0))  # 0-255
    # background
    # screen.blit(background, (0, 0)) # uncommenting becoz its not looking good

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if a keystroke is pressed check whether its right or left and a keystroke is also an event

        if event.type == pygame.KEYDOWN:  # keydown means not the arrow key down it means any key is pressed or not
            if event.key == pygame.K_LEFT:
                Player_x_y_change = -0.2
            if event.key == pygame.K_RIGHT:
                Player_x_y_change = 0.2

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()


                    # get the current x axis of spaceship
                    Bullet_x_axis = Player_x_axis
                    fire_bullet(Bullet_x_axis, Bullet_y_axis)

        if event.type == pygame.KEYUP:  # keyup means checking the key is released or not
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Player_x_y_change = 0
                
        

            # make sure player method is called after the screen.fill otherwise it will not appear on screen

    # checking the boundaries so that our images doesnt go out
    Player_x_axis += Player_x_y_change

    if Player_x_axis <= 0:
        Player_x_axis = 0
    elif Player_x_axis >= 736: # ie 800 - size of aircraft png
        Player_x_axis = 736

    for i in range(num_of_enemies):

        # game over text
        if Enemy_y_axis[i] > 550:
            for j in range(num_of_enemies):
                Enemy_y_axis[j] = 2000
            game_over()
            break

        Enemy_x_axis[i] += Enemy_x_change[i]

        if Enemy_x_axis[i] <= 0:
            Enemy_x_change[i] = 0.1
            Enemy_y_axis[i] += Enemy_y_change[i]

        elif Enemy_x_axis[i] >= 736: # ie 800 - size of aircraft png
            Enemy_x_change[i] = -0.1
            Enemy_y_axis[i] += Enemy_y_change[i]

        # collision
        collision = is_collision(Enemy_x_axis[i], Enemy_y_axis[i], Bullet_x_axis, Bullet_y_axis)
        if collision:

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            
            Bullet_y_axis = 620
            bullet_state = "ready"
            score_value += 1
            Enemy_x_axis[i] = random.randint(0, 736)
            Enemy_y_axis[i] = random.randint(40, 250)
            
        enemy(Enemy_x_axis[i], Enemy_y_axis[i], i)

    # bullet movement
    if Bullet_y_axis <= 0:
        Bullet_y_axis = 620
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(Bullet_x_axis, Bullet_y_axis)
        Bullet_y_axis -= Bullet_y_change

    




    player(Player_x_axis, Player_y_axis)
    
    show_score(txt_x,txt_y)
    pygame.display.update()  # imp line becoz we want it when player is moving, bullet etc
