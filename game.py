import pygame
import constants as co

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

# Icons by Lorc: https://lorcblog.blogspot.com/
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://luizmelo.itch.io/monsters-creatures-fantasy

def load_grid_images(sheet_file, width, height, columns, rows):
  '''
  Load frames/tiles from a sprite sheet.
  
  :param sheet: path of sheet file
  :param width: frame's width
  :param height: frame's height
  :param columns: number of columns in the sheet
  :param rows: number of rows in the sheet
  '''
  sheet_image = pygame.image.load(sheet_file).convert_alpha()
  images = []
  cell_width = sheet_image.get_rect().w / columns
  cell_height = sheet_image.get_rect().h / rows
  x_delta = (cell_width - width) / 2
  y_delta = (cell_height - height) / 2
  for row in range(rows):
    for col in range(columns):
      x = col * cell_width + x_delta
      y = row * cell_height + y_delta
      img = pygame.Surface([width, height], pygame.SRCALPHA)
      img.blit(sheet_image, (0, 0), (x, y, width, height))
      images.append(img)
  return images

class Block(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([co.BLOCK_WIDHT, co.BLOCK_HEIGHT])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)
    self.hit_points = 1

class AmberGoblin(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.idle_frames = [
      pygame.image.load('assets/amber_goblin_idle_frame_000.png').convert_alpha(), 
      pygame.image.load('assets/amber_goblin_idle_frame_001.png').convert_alpha(), 
      pygame.image.load('assets/amber_goblin_idle_frame_002.png').convert_alpha(), 
      pygame.image.load('assets/amber_goblin_idle_frame_003.png').convert_alpha()
    ]
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect()  
    self.mask = pygame.mask.from_surface(self.idle_frames[0])
    self.rect.topleft = (x, y)
    self.hit_points = 1
    self.tick = 1
    self.frame_count = 0

  def update(self):
    TICK_CHANGE = 6
    if self.tick == TICK_CHANGE:
      self.tick = 0
      self.image = self.idle_frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.idle_frames)
    self.tick += 1
  
  def collide(self, ball):
    ball.y_direction *= -1
    self.hit_points -= 1

class Player(pygame.sprite.Sprite):
  def __init__(self, lives=0):
    pygame.sprite.Sprite.__init__(self)
    FRAME_DIM = 115
    # idle frames
    self.idle_right_frames = load_grid_images('assets/player_idle_sheet.png', FRAME_DIM, FRAME_DIM, 6, 1)
    self.idle_right_masks = [pygame.mask.from_surface(img) for img in self.idle_right_frames]
    self.idle_left_frames = [pygame.transform.flip(img, True, False) for img in self.idle_right_frames]
    self.idle_left_masks = [pygame.mask.from_surface(img) for img in self.idle_left_frames]
    # running frames
    self.running_right_frames = load_grid_images('assets/player_run_right_sheet.png', FRAME_DIM, FRAME_DIM, 8, 1)
    self.running_right_masks = [pygame.mask.from_surface(img) for img in self.running_right_frames]
    self.running_left_frames = [pygame.transform.flip(img, True, False) for img in self.running_right_frames]
    self.running_left_masks = [pygame.mask.from_surface(img) for img in self.running_left_frames]
    # initial state
    self.image = self.idle_right_frames[0]
    self.rect = self.image.get_rect()
    self.mask = self.idle_right_masks[0]
    self.lives = lives
    self.speed = 7
    # state variables
    self.IDLE_RIGHT = 0
    self.IDLE_LEFT = 1
    self.RUNNING_LEFT = 2
    self.RUNNING_RIGHT = 3
    self.state = self.IDLE_RIGHT
    self.frame_count = 0
    self.tick = 1

  def to_left(self):
    self.state = self.RUNNING_LEFT
    self.frame_count = 0
    self.tick = 1
  
  def to_right(self):
    self.state = self.RUNNING_RIGHT
    self.frame_count = 0
    self.tick = 1

  def to_idle(self):
    if self.state == self.RUNNING_RIGHT:
      self.state = self.IDLE_RIGHT
    else:
      self.state = self.IDLE_LEFT
    self.frame_count = 0
    self.tick = 1
  
  def _adjust_position(self):
    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > co.SCREEN_WIDHT:
      self.rect.right = co.SCREEN_WIDHT

  def update(self):
    TICK_CHANGE = 6
    if self.state == self.IDLE_RIGHT:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.idle_right_frames[self.frame_count]
        self.mask = self.idle_right_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.idle_right_frames)
    elif self.state == self.IDLE_LEFT:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.idle_left_frames[self.frame_count]
        self.mask = self.idle_left_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.idle_left_frames)
    elif self.state == self.RUNNING_LEFT:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.running_left_frames[self.frame_count]
        self.mask = self.running_left_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_left_frames)
      self.rect.x -= self.speed
      self._adjust_position()
    elif self.state == self.RUNNING_RIGHT:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.running_right_frames[self.frame_count]
        self.mask = self.running_right_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_right_frames)
      self.rect.x += self.speed
      self._adjust_position()
    self.tick += 1

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('assets/mace-head.png').convert_alpha()
    self.image = pygame.transform.scale(img, (co.BALL_SIZE, co.BALL_SIZE))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.x_direction = 1   # 1 for right, -1 for left
    self.y_direction = -1  # 1 for down, -1 for up
    self.speed = 5
  
  def update(self):
    self.rect.left += self.speed * self.x_direction
    self.rect.top += self.speed * self.y_direction
      
class Edge(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([width, height])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)

class Arena:
  # This class is used to check if an sprite reaches the edges of the screen
  def __init__(self):
    self.left_edge = Edge(-1, 0, 1, co.SCREEN_HEIGHT)
    self.right_edge = Edge(co.SCREEN_WIDHT + 1, 0, 1, co.SCREEN_HEIGHT)
    self.top_edge = Edge(0, -1, co.SCREEN_WIDHT, 1)
    self.edges = [self.left_edge, self.right_edge, self.top_edge]
  
  def check_bump(self, ball):
    hitted_edges = pygame.sprite.spritecollide(ball, self.edges, False, pygame.sprite.collide_mask)
    if self.left_edge in hitted_edges or self.right_edge in hitted_edges:
      ball.x_direction *= -1
      ball.rect.left += ball.x_direction * 2
    if self.top_edge in hitted_edges:
      ball.y_direction *= -1
      ball.rect.top += ball.y_direction * 2

  def below_screen(self, sprite):
    return sprite.rect.top > co.SCREEN_HEIGHT


def center_player_and_ball(player, ball):
  player.rect.topleft = (
    co.SCREEN_WIDHT / 2 - player.rect.w / 2, 
    co.SCREEN_HEIGHT - player.rect.h - 5
  )
  t = player.rect.topleft
  ball.rect.topleft = (
    t[0] + player.rect.width / 2, 
    t[1] - 60
  )
  ball.x_direction = 1
  ball.y_direction = -1




### INITIALIZATION ###
pygame.init()
screen = pygame.display.set_mode((co.SCREEN_WIDHT, co.SCREEN_HEIGHT))
pygame.display.set_caption("Fantasy Breaker")

clock = pygame.time.Clock()