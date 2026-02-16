import pygame, game, math
import constants as co

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
  def __init__(self, magical_bar, lives=0):
    pygame.sprite.Sprite.__init__(self)
    FRAME_DIM = 115
    # idle frames
    self.idle_right_frames = game.load_grid_images('assets/player_idle_sheet.png', FRAME_DIM, FRAME_DIM, 6, 1)
    self.idle_right_masks = [pygame.mask.from_surface(img) for img in self.idle_right_frames]
    self.idle_left_frames = [pygame.transform.flip(img, True, False) for img in self.idle_right_frames]
    self.idle_left_masks = [pygame.mask.from_surface(img) for img in self.idle_left_frames]
    # running frames
    self.running_right_frames = game.load_grid_images('assets/player_run_right_sheet.png', FRAME_DIM, FRAME_DIM, 8, 1)
    self.running_right_masks = [pygame.mask.from_surface(img) for img in self.running_right_frames]
    self.running_left_frames = [pygame.transform.flip(img, True, False) for img in self.running_right_frames]
    self.running_left_masks = [pygame.mask.from_surface(img) for img in self.running_left_frames]
    # initial state
    self.image = self.idle_right_frames[0]
    self.rect = self.image.get_rect()
    self.mask = self.idle_right_masks[0]
    self.lives = lives
    self.speed = 7
    self.magical_bar = magical_bar
    # state variables
    self.IDLE_RIGHT = 0
    self.IDLE_LEFT = 1
    self.RUNNING_LEFT = 2
    self.RUNNING_RIGHT = 3
    self.state = self.IDLE_RIGHT
    self.frame_count = 0
    self.tick = 1
  
  def move_to(self, x, y):
    self.rect.topleft = (x, y)
    self.magical_bar.rect.centerx = self.rect.centerx
    self.magical_bar.rect.top = y - 5
    self.magical_bar.angle_pointer.rect.centerx = self.rect.centerx
    self.magical_bar.angle_pointer.rect.bottom = self.magical_bar.rect.top - 3

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
    y = self.rect.y
    if self.rect.left < 0:
      self.move_to(0, y)
    elif self.rect.right > co.SCREEN_WIDHT:
      #self.rect.right = co.SCREEN_WIDHT
      self.move_to(co.SCREEN_WIDHT - self.rect.w, y)

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
      self.magical_bar.rect.x -= self.speed
      self.magical_bar.angle_pointer.rect.x -= self.speed
      self._adjust_position()
    elif self.state == self.RUNNING_RIGHT:
      if self.tick == TICK_CHANGE:
        self.tick = 0
        self.image = self.running_right_frames[self.frame_count]
        self.mask = self.running_right_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_right_frames)
      self.rect.x += self.speed
      self.magical_bar.rect.x += self.speed
      self.magical_bar.angle_pointer.rect.x += self.speed
      self._adjust_position()
    self.tick += 1

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('assets/mace-head.png').convert_alpha()
    self.image = pygame.transform.scale(img, (co.BALL_SIZE, co.BALL_SIZE))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.SPEED = 5
    self.reset_movement()
  
  def reset_movement(self):
    self.y_direction = -1  # 1 for down, -1 for up
    self.x_speed = self.SPEED
    self.y_speed = self.SPEED

  def update(self):
    self.rect.left += self.x_speed
    self.rect.top += self.y_speed * self.y_direction
  
  def reverse_vertical_movement(self):
    self.y_direction *= -1
  
  def reverse_horizontal_movement(self):
    self.x_speed *= -1
      
class Boundary(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([width, height])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)

class Arena:
  # This class is used to check if an sprite reaches the boundaries of the screen
  def __init__(self):
    self.left_boundary = Boundary(-1, 0, 1, co.SCREEN_HEIGHT)
    self.right_boundary = Boundary(co.SCREEN_WIDHT + 1, 0, 1, co.SCREEN_HEIGHT)
    self.top_boundary = Boundary(0, -1, co.SCREEN_WIDHT, 1)
    self.boundaries = [self.left_boundary, self.right_boundary, self.top_boundary]
  
  def check_bump(self, ball):
    hitted_boundaries = pygame.sprite.spritecollide(ball, self.boundaries, False, pygame.sprite.collide_mask)
    if self.left_boundary in hitted_boundaries or self.right_boundary in hitted_boundaries:
      ball.x_speed *= -1
      if ball.x_speed > 0:
        ball.rect.left += 2
      else:
        ball.rect.left -= 2
    if self.top_boundary in hitted_boundaries:
      ball.y_direction *= -1
      ball.rect.top += ball.y_direction * 2

  def below_screen(self, sprite):
    return sprite.rect.top > co.SCREEN_HEIGHT
  
class MagicalBar(pygame.sprite.Sprite):
  def __init__(self, angle_pointer):
    pygame.sprite.Sprite.__init__(self)
    self.frames = game.load_grid_images('assets/magical_bar_sheet.png', 120, 7, 6, 1)
    self.masks = [pygame.mask.from_surface(img) for img in self.frames]
    self.image = self.frames[0]
    self.mask = self.masks[0]
    self.rect = self.image.get_rect()  
    self.tick = 1
    self.frame_count = 0
    self.angle_pointer = angle_pointer

  def update(self):
    TICK_CHANGE = 12
    if self.tick == TICK_CHANGE:
      self.tick = 0
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    self.tick += 1
  
  def collide(self, ball):
    ball.x_speed = ball.y_speed / math.tan(self.angle_pointer.angle)
    ball.reverse_vertical_movement()
    ball.rect.y -= 3
  
  def increase_angle(self):
    delta = min(self.angle_pointer.angle + math.pi / 10, 3 * math.pi / 4)
    self.angle_pointer.angle = delta
  
  def decrease_angle(self):
    delta = max(self.angle_pointer.angle - math.pi / 10, math.pi / 4)
    self.angle_pointer.angle = delta

class AnglePointer(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((40,20),  pygame.SRCALPHA)
    self.rect = self.image.get_rect()
    self.angle = math.pi / 2
    self.increase = False
    self.decrease = False
    self.update()
  
  def update(self):
    self.image.fill((0, 0, 0, 0))
    angle_step = math.pi / 30
    if self.increase:
      alpha = min(self.angle + angle_step, 3 * math.pi / 4)
      self.angle = alpha
    elif self.decrease:
      alpha = max(self.angle - angle_step, math.pi / 4)
      self.angle = alpha
    d = self.rect.h
    x1 = self.rect.w / 2
    y1 = self.rect.h
    x2 = x1 + math.cos(self.angle) * d
    y2 = y1 - math.sin(self.angle) * d
    pygame.draw.line(self.image, '0x30b35f', (x1, y1), (x2, y2), 3)
 
  

