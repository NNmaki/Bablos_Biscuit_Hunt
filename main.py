#
#
# Bablos Biscuit Hunt - Small practice with Python
# By Niko Nmaki 2024
#
# Inspired By @bablo_thedog - https://www.instagram.com/bablo_thedog/
#
#
# Building steps: (just note to myself)
# 1. Import Libraries
# 2. Pygame setup - define canvas size, title etc
# 3. Define background and set position
# 4. Define characters 
# 5. Set coordinates to spawn moving character
# 6. Draw actors and set draw() -function
# 7. Define update() -function which acts like gameloop
# 8. Map keyboard and set key-functions on update() -function
# 9. Set characters moving speed with velocity -variable
# 10. Set player character movement animation
# 11. Define spawn-function for falling object
# 12. Set schedule for object spawning
# 13. Set parameters (velocity) for falling objects
# 14. Add collecting feature with .colliderect() -method
# 15. Make display to show game info and set timer and life counter and score
# 16. Set game_over() -details
# 17. Set start/restart
# 18. Set music and sounds
#
#

import pgzrun # import pygame zero library
from random import randint

velocity = 5
biscuits = []
biscuit_velocity = 5

timer = 0
score = 0
lives = 5

# set canvas size & title (pygame zero constants, not variables)
WIDTH = 580
HEIGHT = 860
TITLE = "Bablo's Biscuit Hunt"

# set objects/actors and positions
bg = Actor("background2")
bg.pos = (WIDTH // 2, HEIGHT // 2)

dog = Actor("bablo_center")
dog.midbottom = (WIDTH // 2, HEIGHT)

biscuit = Actor("biscuit50")
biscuit.x = randint(20, WIDTH - 20)
biscuit.y = randint(20, HEIGHT - 20)

# set draw function to draw objects
def draw():
    screen.clear()
    bg.draw()
    dog.draw()
    for biscuit in biscuits:
        biscuit.draw()

    # draw heads up display:    
    screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=42)
    screen.draw.text(f"Lives: {lives}", midtop=(WIDTH // 2, 10), fontsize=42)
    screen.draw.text(f"Time: {timer}", topright=(WIDTH -10, 10), fontsize=42)


# update function, which acts like game loop
def update():
    global score # set variable global to access it within function
    global lives # set variable global to access it within function
    if keyboard.LEFT and dog.left > 0 :
        dog.x -= velocity
        dog.image = "bablo_left"
    elif keyboard.RIGHT and dog.right < WIDTH:
        dog.x += velocity
        dog.image = "bablo_right"
    if keyboard.UP and dog.top > 0:
        dog.y -= velocity
    elif keyboard.DOWN and dog.bottom < HEIGHT:
        dog.y += velocity
    for biscuit in biscuits:
        biscuit.y += biscuit_velocity # make biscuits falling
        if biscuit.top > HEIGHT: # if top of biscuit goes below the screen
            biscuits.remove(biscuit) # remove it from list
            lives -= 1

        if dog.colliderect(biscuit): # if player "hits" biscuit
            biscuits.remove(biscuit) # remove biscuit from list (and screen)
            score += 1
    

    
# function which is called when key button released and sets forward facing image 
def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        dog.image = "bablo_center"

# define spawning function to spawn falling objects
def spawn_biscuit():
    biscuit = Actor("biscuit")
    biscuit.x = randint(20, WIDTH - 20)
    biscuit.y = -20
    biscuits.append(biscuit)

def increment_timer():
    global timer # set variable global to access it within function
    timer += 1 

clock.schedule_interval(increment_timer, 1.0)
clock.schedule_interval(spawn_biscuit, 0.5)

pgzrun.go() # executes "game loop"
