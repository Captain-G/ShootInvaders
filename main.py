import pygame
import random
import math

from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen and specify the width and height respectively
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("ShootInvaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(0, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# bullet
bullet_image = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 4
bullet_y_change = 10
# ready state - you cant see the bullet on the screen
# fire state - the bullet is currently moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("blackParadeFont.otf", 64)
text_x = 10
text_y = 10

# game over text
over_font = pygame.font.Font("blackParadeFont.otf", 128)


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, j):
    screen.blit(enemy_img[j], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# game loop
running = True
while running:

    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # initially the game window closes after a few seconds
        # this if statement makes it permanent not unless you click on the close button
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether it is right of left
        # keydown is pressing a key while keyup is releasing that key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # checking for boundaries of spaceship so it doesn't go out of bounds
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    # enemy movement
    for j in range(no_of_enemies):
        # game over
        if enemy_y[j] > 440:
            for k in range(no_of_enemies):
                enemy_y[k] = 2000
            game_over_text()
            break

        enemy_x[j] += enemy_x_change[j]

        if enemy_x[j] < 0:
            enemy_x_change[j] = 4
            enemy_y[j] += enemy_y_change[j]
        elif enemy_x[j] >= 736:
            enemy_x_change[j] = -4
            enemy_y[j] += enemy_y_change[j]

            # collision
        collision = is_collision(enemy_x[j], enemy_y[j], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[j] = random.randint(0, 735)
            enemy_y[j] = random.randint(0, 150)
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()

        enemy(enemy_x[j], enemy_y[j], j)

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    # update your screen because things are constantly moving
    pygame.display.update()
