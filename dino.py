try:
  import os
  if hasattr(os, "environ"):
      os.environ['KANDINSKY_OS_MODE'] = '2'
      os.environ['KANDINSKY_NO_GUI'] = ''
      os.environ['KANDINSKY_USE_HEAP'] = ''
except: pass
from time import sleep

from kandinsky import *
from ion import *
from random import randint

COLOR_DARK = color(32, 33, 36)
COLOR_WHITE = color(172, 172, 172)
COLOR_TEST = color(255, 255, 255)
SCREEN_W = 320
SCREEN_H = 222
BASE_DINO_Y = 178 # 183
CROUCHING_HEIGHT = 11
GRAVITY = 0.09
JUMP_HEIGHT = 3.1
DINO_HEIGHT = 25 # 20
DINO_WIDTH = 13
DINO_X = 15
ENTITY_OVERLAPPING_DINO_DISTANCE = 5

dino_y = BASE_DINO_Y

is_jumping = False
is_crouching = False
current_jump_height = JUMP_HEIGHT
is_game_over = False
score = 0
spawned_entity_list = []
max_entity_spawn_delay = randint(50, 200)
entity_spawn_delay = 0
entity_delta = 1.0

CACTUS_HEIGHT = 15
CACTUS_WIDTH = 10
CACTUS_Y = BASE_DINO_Y - (CACTUS_HEIGHT - DINO_HEIGHT)
BIRD_HEIGHT = 9
BIRD_ADDITIONAL_Y = 14

class Entity:
    def __init__(self, x, y, height, width, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.overlapped = False
        self.type = type
        self.animation_time = 0 # only for bird (for now)


def cactus_entity():
    return Entity(SCREEN_W, CACTUS_Y, CACTUS_HEIGHT, CACTUS_WIDTH, "cactus")


def bird_entity(is_high):
    bird_y = BASE_DINO_Y
    if is_high:
        bird_y -= BIRD_ADDITIONAL_Y
    return Entity(SCREEN_W, bird_y, BIRD_HEIGHT, CACTUS_WIDTH, "bird")


def init():
    # background
    fill_rect(0, 0, SCREEN_W, SCREEN_H, COLOR_DARK)
    # dino
    fill_rect(DINO_X, dino_y, DINO_WIDTH, DINO_HEIGHT, COLOR_WHITE)
    # add cactus
    spawned_entity_list.append(cactus_entity())


def jump_fall():
    global current_jump_height, dino_y

    dino_y -= current_jump_height
    fill_rect(DINO_X, int(dino_y + current_jump_height - DINO_HEIGHT), DINO_WIDTH,
              int(DINO_HEIGHT - current_jump_height) - 1, COLOR_DARK)
    fill_rect(DINO_X, int(dino_y - current_jump_height), DINO_WIDTH, int(DINO_HEIGHT + current_jump_height),
              COLOR_WHITE)
    current_jump_height -= GRAVITY


def jump_end():
    global current_jump_height, dino_y, is_jumping

    fill_rect(DINO_X, int(dino_y + current_jump_height), DINO_WIDTH, 50, COLOR_DARK)
    current_jump_height = JUMP_HEIGHT
    dino_y = BASE_DINO_Y
    fill_rect(DINO_X, int(dino_y), DINO_WIDTH, DINO_HEIGHT, COLOR_WHITE)
    is_jumping = False


def jump():
    global current_jump_height, dino_y, is_jumping

    if not current_jump_height < 0:
        dino_y -= current_jump_height
        fill_rect(DINO_X, int(dino_y + current_jump_height + DINO_HEIGHT), DINO_WIDTH, int(current_jump_height) + 1,
                  COLOR_DARK)
        fill_rect(DINO_X, int(dino_y - current_jump_height), DINO_WIDTH, int(DINO_HEIGHT - current_jump_height),
                  COLOR_WHITE)
        current_jump_height -= GRAVITY
    elif not current_jump_height < -JUMP_HEIGHT:
        jump_fall()
    else:
        jump_end()


def draw_level():
    fill_rect(0, 205, 320, 3, COLOR_WHITE)  #draw line
    draw_string(f"score: {score}", 200, 10, COLOR_WHITE, COLOR_DARK)


def update_entity(entity):
    if entity.x < -10:
        spawned_entity_list.remove(entity)
    else:
        entity.x -= entity_delta

        fill_rect(int(entity.x + entity.width), entity.y, entity.width, entity.height, COLOR_DARK)

        entity_color = COLOR_WHITE

        if entity.type == "bird":
            if entity.animation_time < 30:
                entity.height = BIRD_HEIGHT + 4
                entity_color = color(171, 171, 171)
            elif entity.animation_time > 30:
                entity_color = color(171, 171, 171)
                entity.height = BIRD_HEIGHT - 4

            if entity.animation_time >= 70:
                entity_color = color(171, 171, 171)
                entity.animation_time = 0

            entity.animation_time += 1
            if entity_color == COLOR_WHITE: # remove this an see why it's here
                entity_color = COLOR_DARK
        fill_rect(int(entity.x), entity.y, entity.width, entity.height, entity_color)


def listen_key():
    global is_crouching, is_jumping, current_jump_height

    if keydown(KEY_BACKSPACE):
        game_over()

    if keydown(KEY_OK) and is_game_over:
        restart()

    if keydown(KEY_DOWN):
        if is_jumping:
            jump_end()
        else:
            fill_rect(DINO_X, dino_y, DINO_WIDTH, CROUCHING_HEIGHT, COLOR_DARK)
            is_crouching = True
    elif is_crouching:
        fill_rect(DINO_X, dino_y, DINO_WIDTH, CROUCHING_HEIGHT, COLOR_WHITE)
        is_crouching = False
    if keydown(KEY_UP) and not is_jumping and not is_crouching:
        is_jumping = True


def check_collision(entity):
    global is_game_over
    is_overlapping_entity = entity.x - 15 < DINO_X < entity.x + 10
    is_entity_under = dino_y > entity.y - entity.height - 5

    if is_overlapping_entity:
        if entity.type == "bird":
            if not is_crouching and is_entity_under:
                game_over()
        elif is_entity_under:
            game_over()


def game_over():
    global is_game_over
    is_game_over = True
    spawned_entity_list.clear()

    text_x = 118
    text_y = 40
    draw_string("Game Over", text_x, text_y, COLOR_WHITE, COLOR_DARK)
    fill_rect(140, 60, 50, 40, COLOR_WHITE)
    fill_rect(155, 71, 20, 17, COLOR_DARK)
    fill_rect(158, 75, 14, 10, COLOR_WHITE)

    set_pixel(155, 86, COLOR_WHITE)
    set_pixel(155, 87, COLOR_WHITE)
    set_pixel(156, 87, COLOR_WHITE)

    set_pixel(174, 86, COLOR_WHITE)
    set_pixel(174, 87, COLOR_WHITE)
    set_pixel(173, 87, COLOR_WHITE)

def restart():
    global is_game_over, dino_y, score, entity_delta
    is_game_over = False
    dino_y = BASE_DINO_Y
    score = 0
    entity_delta = 1.0
    init()


init()
game_over()
while True:
    sleep(0.005)
    listen_key()

    if not is_game_over:
        draw_level()
        for entity in spawned_entity_list:
            check_collision(entity)
            update_entity(entity)

            if DINO_X - entity.x > ENTITY_OVERLAPPING_DINO_DISTANCE and not entity.overlapped:
                entity.overlapped = True
                score += 1
                if entity_delta < 4.6 and score % 5 == 1:
                    entity_delta += 0.2

        if is_jumping:
            jump()

        if entity_spawn_delay >= max_entity_spawn_delay:
            if score > 20:
                bird_spawn_probability = randint(1, 4)

                if bird_spawn_probability == 1:
                    # spawn a bird
                    is_high = True
                    spawned_entity_list.append(bird_entity(is_high))
                else:
                    # spawn a cactus
                    spawned_entity_list.append(cactus_entity())
            else:
                spawned_entity_list.append(cactus_entity())
            max_entity_spawn_delay = randint(50, 200)
            entity_spawn_delay = 0
        else:
            entity_spawn_delay += 1
