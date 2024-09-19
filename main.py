#
# Bablos Biscuit Hunt - Small practice with Python
# By Niko Nmaki 2024
#
# https://github.com/NNmaki/Bablos_Biscuit_Hunt
#
# Inspired By @bablo_thedog - https://www.instagram.com/bablo_thedog/
#
import pygame
from pygame.locals import *
from random import randint
import os
import sys

pygame.init()

# Set variables
velocity = 8
biscuits = []
biscuit_velocity = 3
carrots = []
carrot_velocity = 4
olives = []
olive_velocity = 4
sausages = []
sausage_velocity = 2

timer = 0
score = 0
lives = 5
over = False
FPS = 60

in_menu = True
instructions = False

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
menu_bg = pygame.image.load(resource_path("images/menu_backround.png"))
button_play = pygame.image.load(resource_path("images/button_play.png"))
button_instructions = pygame.image.load(resource_path("images/button_instructions.png"))
button_quit = pygame.image.load(resource_path("images/button_quit.png"))
instructions_image = pygame.image.load(resource_path("images/instructions.png"))
dog_images = {
    "center": pygame.image.load(resource_path("images/bablo_center.png")),
    "left": pygame.image.load(resource_path("images/bablo_left.png")),
    "right": pygame.image.load(resource_path("images/bablo_right.png"))
}
dog = dog_images["center"]
dog_rect = dog.get_rect(midbottom=(WIDTH // 2, HEIGHT))
biscuit_image = pygame.image.load(resource_path("images/biscuit50.png"))
carrot_image = pygame.image.load(resource_path("images/carrot50.png"))
olive_image = pygame.image.load(resource_path("images/olive50.png"))
sausage_image = pygame.image.load(resource_path("images/sausage50.png"))

# Load sounds
bark_sound = pygame.mixer.Sound(resource_path("sounds/bark.wav"))
barktwice_sound = pygame.mixer.Sound(resource_path("sounds/barktwice.wav"))
pygame.mixer.music.load(resource_path("music/biscuithunt.mp3"))
pygame.mixer.music.load(resource_path("music/menumusic.mp3"))

# Set fonts
font = pygame.font.SysFont(None, 42)
font_game_over = pygame.font.SysFont(None, 100)

# Set timers
clock = pygame.time.Clock()
biscuit_spawn_event = pygame.USEREVENT + 1
timer_event = pygame.USEREVENT + 2
restart_event = pygame.USEREVENT + 3 # New event for restarting game
carrot_spawn_event = pygame.USEREVENT + 4
olive_spawn_event = pygame.USEREVENT +5
sausage_spawn_event = pygame.USEREVENT +6
pygame.time.set_timer(biscuit_spawn_event, 500)
pygame.time.set_timer(carrot_spawn_event, 2000)
pygame.time.set_timer(olive_spawn_event, 2000)
pygame.time.set_timer(sausage_spawn_event, 6000)
pygame.time.set_timer(timer_event, 1000)

def draw():
    screen.blit(bg, (0, 0))
    screen.blit(dog, dog_rect)
    for biscuit_rect in biscuits:
        screen.blit(biscuit_image, biscuit_rect)
    for carrot_rect in carrots:
        screen.blit(carrot_image, carrot_rect)
    for olive_rect in olives:
        screen.blit(olive_image, olive_rect)
    for sausage_rect in sausages:
        screen.blit(sausage_image, sausage_rect)

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

# Define function to draw start menu
def draw_menu():
    screen.blit(menu_bg, (0,0))
    button_rect = button_play.get_rect(center=(WIDTH // 2, HEIGHT // 2 -50))
    screen.blit(button_play, button_rect)
    
    button_rect2 = button_instructions.get_rect(center=(WIDTH // 2 -150, HEIGHT // 2 +90))
    screen.blit(button_instructions, button_rect2)

    button_rect3 = button_quit.get_rect(center=(WIDTH // 2 +150, HEIGHT // 2 +90))
    screen.blit(button_quit, button_rect3)

def instructions_menu():
    instructions_rect = instructions_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(instructions_image, instructions_rect)

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

    for carrot_rect in carrots[:]:
        carrot_rect.y += carrot_velocity
        if carrot_rect.top > HEIGHT:
            carrots.remove(carrot_rect)
        if dog_rect.colliderect(carrot_rect):
            score -= 1
            carrots.remove(carrot_rect)

    for olive_rect in olives[:]:
        olive_rect.y += olive_velocity
        if olive_rect.top > HEIGHT:
            olives.remove(olive_rect)
        if dog_rect.colliderect(olive_rect):
            score -= 2
            olives.remove(olive_rect)

    for sausage_rect in sausages[:]:
        sausage_rect.y += sausage_velocity
        if sausage_rect.top > HEIGHT:
            sausages.remove(sausage_rect)
        if dog_rect.colliderect(sausage_rect):
            lives = 0
            sausages.remove(sausage_rect)
            game_over()
            
    if lives <= 0 and not over:
        barktwice_sound.play()
        game_over()

def update_dog_image(direction):
    global dog
    dog = dog_images[direction]

def spawn_biscuit():
    biscuit_rect = biscuit_image.get_rect(midtop=(randint(20, WIDTH - 20), -20))
    biscuits.append(biscuit_rect)

def spawn_carrot():
    carrot_rect = carrot_image.get_rect(midtop=(randint(20, WIDTH -20), -20))
    carrots.append(carrot_rect)

def spawn_olive():
    olive_rect = olive_image.get_rect(midtop=(randint(20, WIDTH -20), -20))
    olives.append(olive_rect)

def spawn_sausage():
    sausage_rect = sausage_image.get_rect(midtop=(randint(20, WIDTH -20), -20))
    sausages.append(sausage_rect)

def game_over():
    global over, in_menu
    over = True
    pygame.time.set_timer(biscuit_spawn_event, 0)
    pygame.time.set_timer(carrot_spawn_event, 0)
    pygame.time.set_timer(olive_spawn_event, 0)
    pygame.time.set_timer(sausage_spawn_event, 0)
    pygame.time.set_timer(timer_event, 0)
    pygame.mixer.music.stop()
    pygame.time.set_timer(restart_event, 5000, True)

def start():
    global timer, score, lives, biscuit_velocity, carrot_velocity, olive_velocity, sausage_velocity, velocity, over
    over = False
    timer = 0
    score = 0
    lives = 5
    biscuit_velocity = 3
    carrot_velocity = 4
    olive_velocity = 4
    sausage_velocity = 2
    velocity = 8
    biscuits.clear()
    carrots.clear()
    olives.clear()
    sausages.clear()
    dog_rect.midbottom = (WIDTH // 2, HEIGHT)
    pygame.time.set_timer(biscuit_spawn_event, 500)
    pygame.time.set_timer(carrot_spawn_event, 2000)
    pygame.time.set_timer(olive_spawn_event, 2000)
    pygame.time.set_timer(sausage_spawn_event, 6000)
    pygame.time.set_timer(timer_event, 1000)
    barktwice_sound.play()
    # barktwice_sound.play(loops=1)
    # pygame.mixer.music.play(-1)  # Set music playing constanly

# Game Loop
start()
running = True
game_music_playing = False # States if game music is playing
menu_music_playing = False # States if game music is playing

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYUP:
            if event.key == K_SPACE and in_menu:
                start()
                in_menu = False
            elif event.key in (K_LEFT, K_RIGHT):
                update_dog_image("center")
            if event.key == K_i and in_menu:
                instructions = True
            if event.key == K_ESCAPE and in_menu:
                instructions = False
            if event.key == K_ESCAPE and running:
                in_menu = True
            if event.key == K_q and in_menu:
                running = False
        elif event.type == biscuit_spawn_event:
            spawn_biscuit()
        elif event.type == carrot_spawn_event:
            spawn_carrot()
        elif event.type == olive_spawn_event:
            spawn_olive()
        elif event.type == sausage_spawn_event:
            spawn_sausage()
        elif event.type == timer_event:
            timer += 1
        elif event.type == restart_event:
            in_menu = True # Back to menu-screen
           
    if in_menu: # Show menu if in_menu = True
        draw_menu()
        if instructions: # Show instructions both of these = True
            instructions_menu()
        
        if not menu_music_playing:
            pygame.mixer.music.load(resource_path("music/menumusic.mp3"))
            pygame.mixer.music.play(-1)
            game_music_playing = False
            menu_music_playing = True

    else:
        update()
        draw()
        if not game_music_playing:
            pygame.mixer.music.load(resource_path("music/biscuithunt.mp3"))
            pygame.mixer.music.play(-1)
            music_playing = True
            menu_music_playing = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()