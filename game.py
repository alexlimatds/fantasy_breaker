import pygame

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

# Icons by Lorc: https://lorcblog.blogspot.com/
# https://opengameart.org/content/dungeon-crawl-32x32-tiles

class Block(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([BLOCK_WIDHT, BLOCK_HEIGHT])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)
    self.hit_points = 1

class Player(pygame.sprite.Sprite):
  def __init__(self, lives=0):
    pygame.sprite.Sprite.__init__(self)
    self.running_left_frames = [
      pygame.image.load('assets/player_run_left_frame_000.png').convert_alpha(), 
      pygame.image.load('assets/player_run_left_frame_001.png').convert_alpha(), 
      pygame.image.load('assets/player_run_left_frame_002.png').convert_alpha(), 
      pygame.image.load('assets/player_run_left_frame_003.png').convert_alpha()
    ]
    self.running_left_masks = [pygame.mask.from_surface(img) for img in self.running_left_frames]
    self.running_right_frames = [
      pygame.image.load('assets/player_run_right_frame_000.png').convert_alpha(), 
      pygame.image.load('assets/player_run_right_frame_001.png').convert_alpha(), 
      pygame.image.load('assets/player_run_right_frame_002.png').convert_alpha(), 
      pygame.image.load('assets/player_run_right_frame_003.png').convert_alpha()
    ]
    self.running_right_masks = [pygame.mask.from_surface(img) for img in self.running_right_frames]
    self.aura_frames = [
      pygame.image.load('assets/player_aura_frame_001.png').convert_alpha(), 
      pygame.image.load('assets/player_aura_frame_002.png').convert_alpha()
    ]
    self.aura_masks = [pygame.mask.from_surface(img) for img in self.aura_frames]
    self.idle_frame = pygame.image.load('assets/player_idle.png').convert_alpha()
    self.idle_mask = pygame.mask.from_surface(self.idle_frame)

    self.image = self.idle_frame
    self.rect = self.image.get_rect()
    self.mask = self.idle_mask
    self.lives = lives
    self.speed = 7
    # state variables
    self.IDLE = 0
    self.RUNNING_LEFT = 1
    self.RUNNING_RIGHT = 2
    self.AURA = 3
    self.state = self.IDLE
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
    self.state = self.IDLE
    self.frame_count = 0
    self.tick = 1
  
  def to_aura(self):
    self.state = self.AURA
    self.frame_count = 0
    self.tick = 1
  
  def _adjust_position(self):
    if self.rect.left < 0:
      self.rect.left = 0
    elif self.rect.right > SCREEN_WIDHT:
      self.rect.right = SCREEN_WIDHT

  def update(self):
    TICK_CHANGE = 6
    if self.state == self.IDLE:
      self.image = self.idle_frame
    elif self.state == self.RUNNING_LEFT:
      self.rect.x -= self.speed
      self._adjust_position()
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.running_left_frames[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_left_frames)
    elif self.state == self.RUNNING_RIGHT:
      self.rect.x += self.speed
      self._adjust_position()
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.running_right_frames[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_right_frames)
    elif self.state == self.AURA:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.aura_frames[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.aura_frames)
    self.tick += 1

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('assets/mace-head.png').convert_alpha()
    self.image = pygame.transform.scale(img, (BALL_SIZE, BALL_SIZE))
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
    self.left_edge = Edge(-1, 0, 1, SCREEN_HEIGHT)
    self.right_edge = Edge(SCREEN_WIDHT + 1, 0, 1, SCREEN_HEIGHT)
    self.top_edge = Edge(0, -1, SCREEN_WIDHT, 1)
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
    return sprite.rect.top > SCREEN_HEIGHT


def center_player_and_ball(player, ball):
  player.rect.topleft = (
    SCREEN_WIDHT / 2 - BLOCK_WIDHT / 2, 
    SCREEN_HEIGHT - 65
  )
  t = player.rect.topleft
  ball.rect.topleft = (
    t[0] + player.rect.width / 2, 
    t[1] - 60
  )
  ball.x_direction = 1
  ball.y_direction = -1


### CONSTANTS ###
SCREEN_WIDHT = 600
SCREEN_HEIGHT = 600

BLOCK_WIDHT = 50
BLOCK_HEIGHT = 20

BALL_SIZE = 40

### INITIALIZATION ###
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Fantasy Breaker")

clock = pygame.time.Clock()