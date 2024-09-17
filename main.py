#
#
#
# Bablos Biscuit Hunt - Small practice with Python
# By Niko Nmaki 2024
#
# Inspired By @bablo_thedog - https://www.instagram.com/bablo_thedog/
#
#
#

import pygame
from pygame.locals import *
from random import randint

import os
import sys

pygame.init()

# Set variablers
velocity = 17
biscuits = []
biscuit_velocity = 18

timer = 0
score = 0
lives = 5
over = False
FPS = 60

# Set canvas and screen
WIDTH = 580
HEIGHT = 860
TITLE = "Bablo's Biscuit Hunt"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Function to help pyinstaller to find paths
def resource_path(relative_path):
    try: # Pyinstaller to set sys._MEIPASS
            base_path = sys._MEIPASS 
    except AttributeError: # Or use current directory
             base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load images
bg = pygame.image.load(resource_path("images/background2.png"))
dog_images = {
    "center": pygame.image.load(resource_path("images/bablo_center.png")),
    "left": pygame.image.load(resource_path("images/bablo_left.png")),
    "right": pygame.image.load(resource_path("images/bablo_right.png"))
}
dog = dog_images["center"]
dog_rect = dog.get_rect(midbottom=(WIDTH // 2, HEIGHT))

biscuit_image = pygame.image.load(resource_path("images/biscuit50.png"))

# Load sounds
bark_sound = pygame.mixer.Sound(resource_path("sounds/bark.wav"))
barktwice_sound = pygame.mixer.Sound(resource_path("sounds/barktwice.wav"))
pygame.mixer.music.load(resource_path("music/biscuithunt.mp3"))

# Set fonts
font = pygame.font.SysFont(None, 42)
font_game_over = pygame.font.SysFont(None, 100)

# Set timers
clock = pygame.time.Clock()
biscuit_spawn_event = pygame.USEREVENT + 1
timer_event = pygame.USEREVENT + 2
restart_event = pygame.USEREVENT + 3 # New event for restarting game
pygame.time.set_timer(biscuit_spawn_event, 500)
pygame.time.set_timer(timer_event, 1000)

def draw():
    screen.blit(bg, (0, 0))
    screen.blit(dog, dog_rect)

    for biscuit_rect in biscuits:
        screen.blit(biscuit_image, biscuit_rect)

    # Draw heads up display
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    time_text = font.render(f"Time: {timer}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, 10))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    if over:
        game_over_text = font_game_over.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

def update():
    global over, score, lives
    keys = pygame.key.get_pressed()

    # Define Bablos moving
    if keys[K_LEFT] and dog_rect.left > 0:
        dog_rect.x -= velocity
        update_dog_image("left")
    elif keys[K_RIGHT] and dog_rect.right < WIDTH:
        dog_rect.x += velocity
        update_dog_image("right")
    if keys[K_UP] and dog_rect.top > 0:
        dog_rect.y -= velocity
    elif keys[K_DOWN] and dog_rect.bottom < HEIGHT:
        dog_rect.y += velocity

    # Define objects falling and collecting feature
    for biscuit_rect in biscuits[:]:
        biscuit_rect.y += biscuit_velocity
        if biscuit_rect.top > HEIGHT:
            biscuits.remove(biscuit_rect)
            if lives > 0:
                lives -= 1
        if dog_rect.colliderect(biscuit_rect):
            biscuits.remove(biscuit_rect)
            score += 1
            bark_sound.play()

    if lives <= 0 and not over:
        barktwice_sound.play()
        game_over()

def update_dog_image(direction):
    global dog
    dog = dog_images[direction]

def spawn_biscuit():
    biscuit_rect = biscuit_image.get_rect(midtop=(randint(20, WIDTH - 20), -20))
    biscuits.append(biscuit_rect)

def game_over():
    global over
    over = True
    pygame.time.set_timer(biscuit_spawn_event, 0)
    pygame.time.set_timer(timer_event, 0)
    pygame.mixer.music.stop()
    pygame.time.set_timer(restart_event, 5000, True)  # New method for restarting game

def start():
    global timer, score, lives, biscuit_velocity, velocity, over
    over = False
    timer = 0
    score = 0
    lives = 5
    biscuit_velocity = 18
    velocity = 17
    biscuits.clear()
    dog_rect.midbottom = (WIDTH // 2, HEIGHT)
    pygame.time.set_timer(biscuit_spawn_event, 500)
    pygame.time.set_timer(timer_event, 1000)
    pygame.mixer.music.play(-1)  # Set music playing constanly

# Game Loop
start()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                update_dog_image("center")
        elif event.type == biscuit_spawn_event:
            spawn_biscuit()
        elif event.type == timer_event:
            timer += 1
        elif event.type == restart_event:
            start()

        # old restart codes, does not work
        # elif event.type == pygame.USEREVENT + 3:  
            #start()

    update()
    draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
