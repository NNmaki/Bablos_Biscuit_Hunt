
import pygame
from pygame.locals import *
from random import randint

pygame.init()

# Pelin muuttujat
velocity = 5
biscuits = []
biscuit_velocity = 6

timer = 0
score = 0
lives = 5
over = False

# Näytön koko
WIDTH = 580
HEIGHT = 860
TITLE = "Bablo's Biscuit Hunt"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Ladataan kuvat
bg = pygame.image.load("background2.png")
dog_images = {
    "center": pygame.image.load("bablo_center.png"),
    "left": pygame.image.load("bablo_left.png"),
    "right": pygame.image.load("bablo_right.png")
}
dog = dog_images["center"]
dog_rect = dog.get_rect(midbottom=(WIDTH // 2, HEIGHT))

biscuit_image = pygame.image.load("biscuit50.png")

# Äänet
bark_sound = pygame.mixer.Sound("bark.wav")
barktwice_sound = pygame.mixer.Sound("barktwice.wav")
pygame.mixer.music.load("biscuithunt.mp3")

# Fontti
font = pygame.font.SysFont(None, 42)

# Ajastimet
clock = pygame.time.Clock()
biscuit_spawn_event = pygame.USEREVENT + 1
timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(biscuit_spawn_event, 500)
pygame.time.set_timer(timer_event, 1000)

def draw():
    screen.blit(bg, (0, 0))
    screen.blit(dog, dog_rect)

    for biscuit_rect in biscuits:
        screen.blit(biscuit_image, biscuit_rect)

    # Piirrä tekstit
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    time_text = font.render(f"Time: {timer}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, 10))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    if over:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

def update():
    global over, score, lives
    keys = pygame.key.get_pressed()

    # Liikutetaan koiraa
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

    # Liikutetaan keksejä ja tarkistetaan törmäykset
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
    pygame.time.set_timer(pygame.USEREVENT + 3, 5000)  # Ajastetaan pelin uudelleenkäynnistys

def start():
    global timer, score, lives, biscuit_velocity, velocity, over
    over = False
    timer = 0
    score = 0
    lives = 5
    biscuit_velocity = 6
    velocity = 5
    biscuits.clear()
    dog_rect.midbottom = (WIDTH // 2, HEIGHT)
    pygame.time.set_timer(biscuit_spawn_event, 500)
    pygame.time.set_timer(timer_event, 1000)
    pygame.mixer.music.play(-1)  # Toistetaan musiikkia loputtomasti

# Pelin päälooppi
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
        elif event.type == pygame.USEREVENT + 3:  # Uudelleenkäynnistys 5 sekunnin jälkeen
            start()

    update()
    draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
