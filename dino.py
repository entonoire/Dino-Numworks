from kandinsky import *
from ion import *
from random import randint

COLOR_DARK = color(32,33,36)
COLOR_WHITE = color(172,172,172)
COLOR_TEST = color(255, 255, 255)
SCREEN_W = 320
SCREEN_H = 222
BASE_DINO_Y = 183 #base dino position
CROUCHING_HEIGHT = 11
GRAVITY = 0.09
JUMP_HEIGHT = 3.1
DINO_WIDTH = 13
DINO_X = 15
ENTITY_OVERLAPPING_DINO_DISTANCE = 5

dino_y = BASE_DINO_Y
dino_height = 20

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
CACTUS_Y = BASE_DINO_Y - (CACTUS_HEIGHT - dino_height)
BIRD_HEIGHT = 5
class Entity:
  def __init__(self, x, y, shape):
    self.x = x
    self.y = y
    self.shape = shape
    self.width = len(self.shape[0])
    self.height = len(self.shape)
    self.overlapped = False

  def draw(self, color):
    delta_y = self.y
    for shape_y in range(self.height):
      delta_x = self.x
      for shape_x in range(self.width):
        if shape_x == 1 :
          set_pixel(int(delta_x), int(delta_y), color)
        delta_x += 1
      delta_y += 1

def cactus_entity():
  """shape = [
    [[0], [0], [1], [1], [0], [0]],
    [[0], [0], [1], [1], [1], [1]],
    [[1], [0], [1], [1], [1], [1]],
    [[1], [0], [1], [1], [1], [1]],
    [[1], [1], [1], [1], [0], [0]],
    [[0], [0], [1], [1], [0], [0]],
    [[0], [0], [1], [1], [0], [0]],
    [[0], [0], [1], [1], [0], [0]],
    [[0], [0], [1], [1], [0], [0]],
  ]"""
  shape = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  ]
  return Entity(SCREEN_W, CACTUS_Y, shape)

def bird_entity():
  return Entity(SCREEN_W, BASE_DINO_Y, [[1], [1], [1], [1]])

def init():
  # background
  fill_rect(0, 0, SCREEN_W, SCREEN_H, COLOR_DARK)
  # dino
  fill_rect(DINO_X, dino_y, DINO_WIDTH, dino_height, COLOR_WHITE)
  # add cactus
  spawned_entity_list.append(cactus_entity())

def jump_fall():
  global current_jump_height, dino_y

  dino_y -= current_jump_height
  fill_rect(DINO_X, int(dino_y + current_jump_height - dino_height), DINO_WIDTH, int(dino_height - current_jump_height) - 1, COLOR_DARK)
  fill_rect(DINO_X, int(dino_y - current_jump_height), DINO_WIDTH, int(dino_height + current_jump_height), COLOR_WHITE)
  current_jump_height -= GRAVITY

def jump_end():
  global current_jump_height, dino_y, is_jumping

  fill_rect(DINO_X, int(dino_y + current_jump_height), DINO_WIDTH, 50 , COLOR_DARK)
  current_jump_height = JUMP_HEIGHT
  dino_y = BASE_DINO_Y
  fill_rect(DINO_X, int(dino_y), DINO_WIDTH, dino_height, COLOR_WHITE)
  is_jumping = False

def jump():
  global current_jump_height, dino_y, is_jumping

  if not current_jump_height < 0:
    #jumping
    dino_y -= current_jump_height
    fill_rect(DINO_X, int(dino_y + current_jump_height + dino_height), DINO_WIDTH, int(current_jump_height) + 1, COLOR_DARK)
    fill_rect(DINO_X, int(dino_y - current_jump_height), DINO_WIDTH, int(dino_height - current_jump_height), COLOR_WHITE)
    current_jump_height -= GRAVITY
  elif not current_jump_height < -JUMP_HEIGHT:
    jump_fall()
  else:
    jump_end()

def draw_level():
  fill_rect(0, 205, 320, 3, COLOR_WHITE) #draw line
  draw_string(f"score: {score}", 200, 10, COLOR_WHITE, COLOR_DARK)

def update_entity(entity):
  if entity.x < -10:
    spawned_entity_list.remove(entity)
  else:
    entity.draw(COLOR_DARK)
    entity.x -= entity_delta
    entity.draw(COLOR_WHITE)

#  fill_rect(int(entity.x + entity.width), entity.y, entity.width, entity.height, COLOR_DARK)
#  fill_rect(int(entity.x), entity.y, entity.width, entity.height, COLOR_WHITE)

def listen_key():
  global is_crouching, is_jumping, current_jump_height

  if keydown(KEY_BACKSPACE):
    game_over()

  if is_game_over:
    if keydown(KEY_OK):
      restart()
  else:
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
  is_overlapping_entity = entity.x-15 < DINO_X < entity.x+10
  is_entity_under = dino_y > entity.y-entity.height-5

  if is_overlapping_entity:
    if entity.height == BIRD_HEIGHT:
      if not is_crouching and is_entity_under:
        game_over()
      game_over()

def game_over():
  global is_game_over
  is_game_over = True
  spawned_entity_list.clear()

  text_x = 110
  text_y = 40
  draw_string("Game Over", text_x, text_y, COLOR_WHITE, COLOR_DARK)
  fill_rect(140, 60, 50, 40, COLOR_WHITE)
  for i in range(140, 150):
    set_pixel(i, 60, COLOR_DARK)

def restart():
  global is_game_over, dino_y, score
  is_game_over = False
  dino_y = BASE_DINO_Y
  score = 0
  init()

init()
while True:
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
          spawned_entity_list.append(bird_entity())
        else:
          # spawn a cactus
          spawned_entity_list.append(cactus_entity())
      else:
        spawned_entity_list.append(cactus_entity())
      max_entity_spawn_delay = randint(50, 200)
      entity_spawn_delay = 0
    else:
      entity_spawn_delay += 1
