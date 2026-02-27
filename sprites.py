import pygame, util, math, random
import constants as co

class BrickBlock(pygame.sprite.Sprite):
  def __init__(self, center_x, y):
    pygame.sprite.Sprite.__init__(self)
    self.frames = util.load_grid_images(
      'assets/brick_block_sheet.png', 
      co.BLOCK_WIDTH, co.BLOCK_HEIGHT, 
      2, 1
    )
    self.image = self.frames[0]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.midtop = (center_x, y)
    self.hit_points = 2
  
  def collide(self, ball, direction):
    self.hit_points -= ball.strength
    if self.hit_points <= 0:
      self.kill()
    else:
      self.image = self.frames[1]
    util.reverse_ball_direction(ball, direction)


class ConcreteBlock(pygame.sprite.Sprite):
  def __init__(self, center_x, y):
    pygame.sprite.Sprite.__init__(self)
    self.frames = util.load_grid_images(
      'assets/concrete_block_sheet.png', 
      co.BLOCK_WIDTH, co.BLOCK_HEIGHT, 
      3, 1
    )
    self.image = self.frames[0]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.midtop = (center_x, y)
    self.hit_points = 4
  
  def collide(self, ball, direction):
    self.hit_points -= ball.strength
    if self.hit_points <= 0:
      self.kill()
    elif 3 <= self.hit_points <= 4:
      self.image = self.frames[1]
    else:
      self.image = self.frames[2]
    util.reverse_ball_direction(ball, direction)

class EnergyBlock(pygame.sprite.Sprite):
  def __init__(self, center_x, y):
    pygame.sprite.Sprite.__init__(self)
    self.frames = util.load_grid_images(
      'assets/energy_block_sheet.png', 
      co.BLOCK_WIDTH, co.BLOCK_HEIGHT, 
      6, 1
    )
    self.image = self.frames[0]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.midtop = (center_x, y)
    # animation variables
    self.tick = 1
    self.frame_count = 0
  
  def collide(self, ball, direction):
    # This block is indestructible
    util.reverse_ball_direction(ball, direction)

  def update(self, *args, **kwargs):
    # animation
    TICK_CHANGE = 12
    if self.tick == TICK_CHANGE:
      self.tick = 1
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    self.tick += 1

class BloodBLock(pygame.sprite.Sprite):
  def __init__(self, center_x, y):
    # loading frames
    pygame.sprite.Sprite.__init__(self)
    self.idle_frames = util.load_grid_images(
      'assets/blood_block_idle_sheet.png', 
      co.BLOCK_WIDTH, co.BLOCK_HEIGHT, 
      6, 1
    )
    self.hit_frames = util.load_grid_images(
      'assets/blood_block_hit_sheet.png', 
      co.BLOCK_WIDTH, co.BLOCK_HEIGHT, 
      4, 1
    )
    # initial state
    self.frames = self.idle_frames
    self.image = self.frames[0]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.midtop = (center_x, y)
    # animation variables
    self.tick = 1
    self.frame_count = 1
    self.IDLE = 1
    self.HIT = 2
    self.to_idle_state()
  
  def collide(self, ball, direction):
    # This sprite is indestructible
    util.reverse_ball_direction(ball, direction)
    ball.accelerate()
    self.to_hit_state()
  
  def to_hit_state(self):
    self.state = self.HIT
    self.frames = self.hit_frames
    self.frame_count = 0
    self.update_image()
    self.tick = 1
  
  def to_idle_state(self):
    self.state = self.IDLE
    self.frames = self.idle_frames
    self.frame_count = 0
    self.update_image()
    self.tick = 1

  def update_image(self):
    self.image = self.frames[self.frame_count]

  def update_frame(self):
    self.update_image()
    
  def update(self, *args, **kwargs):
    # animation
    if self.state == self.IDLE:
      if self.tick % 12 == 0:
        self.update_image()
        self.frame_count = (self.frame_count + 1) % len(self.frames)
    else: # hit
      TICK_CHANGE = 10
      if self.tick % TICK_CHANGE == 0 and self.frame_count == 4:
        self.to_idle_state()
      elif self.tick % TICK_CHANGE == 0:
        self.update_image()
        self.frame_count += 1
    self.tick += 1

class AmberGoblin(pygame.sprite.Sprite):
  def __init__(self, centerx, top):
    pygame.sprite.Sprite.__init__(self)
    self.idle_frames = util.load_grid_images(
      'assets/amber_goblin_idle_sheet.png', 
      co.AMBLER_GOBLIN_FRAME_DIM, co.AMBLER_GOBLIN_FRAME_DIM, 
      4, 1
    )
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect()  
    self.mask = pygame.mask.from_surface(self.idle_frames[0])
    self.rect.midtop = (centerx, top)
    self.hit_points = 1
    self.tick = random.randint(0, 110)
    self.frame_count = random.randint(0, len(self.idle_frames) - 1)
    self.attack = util.create_dagger(self.rect.centerx, self.rect.bottom + 5)

  def update(self, *args, **kwargs):
    TICK_ANIMATION = 6
    TICK_PROJECTILE = 120
    if self.tick % TICK_ANIMATION == 0:
      self.image = self.idle_frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.idle_frames)
    if self.tick % TICK_PROJECTILE == 0:
      self.attack.throw()
    self.tick += 1
  
  def collide(self, ball, direction):
    self.hit_points -= ball.strength
    if self.hit_points <= 0:
      self.kill()
    util.reverse_ball_direction(ball, direction)

class Player(pygame.sprite.Sprite):
  def __init__(self, magical_bar, lives=0):
    pygame.sprite.Sprite.__init__(self)
    # idle frames
    self.idle_right_frames = util.load_grid_images('assets/player_idle_sheet.png', co.PLAYER_FRAME_DIM, co.PLAYER_FRAME_DIM, 6, 1)
    self.idle_right_masks = [pygame.mask.from_surface(img) for img in self.idle_right_frames]
    self.idle_left_frames = [pygame.transform.flip(img, True, False) for img in self.idle_right_frames]
    self.idle_left_masks = [pygame.mask.from_surface(img) for img in self.idle_left_frames]
    # running frames
    self.running_right_frames = util.load_grid_images('assets/player_run_right_sheet.png', co.PLAYER_FRAME_DIM, co.PLAYER_FRAME_DIM, 8, 1)
    self.running_right_masks = [pygame.mask.from_surface(img) for img in self.running_right_frames]
    self.running_left_frames = [pygame.transform.flip(img, True, False) for img in self.running_right_frames]
    self.running_left_masks = [pygame.mask.from_surface(img) for img in self.running_left_frames]
    # initial state
    self.rect = self.idle_right_frames[0].get_rect()
    self.lives = lives
    self.speed = 7
    self.magical_bar = magical_bar
    # animation
    self.IDLE_RIGHT = 0
    self.IDLE_LEFT = 1
    self.RUNNING_LEFT = 2
    self.RUNNING_RIGHT = 3
    self.to_initial_stance()
    self.TICK_CHANGE = 6
  
  def to_initial_stance(self):
    self.image = self.idle_right_frames[0]
    self.mask = self.idle_right_masks[0]
    self.RUNNING_RIGHT = 3
    self.state = self.IDLE_RIGHT
    self.frame_count = 0
    self.tick = 1
    self.magical_bar.angle_pointer.to_initial_angle()

  def move_to(self, x, y):
    self.rect.topleft = (x, y)
    self.magical_bar.rect.centerx = self.rect.centerx
    self.magical_bar.rect.top = y - 5
    self.magical_bar.angle_pointer.rect.centerx = self.rect.centerx
    self.magical_bar.angle_pointer.rect.bottom = self.magical_bar.rect.top - 3

  def to_left(self):
    if self.state != self.RUNNING_LEFT:
      self.state = self.RUNNING_LEFT
      self.frame_count = 0
      self.tick = self.TICK_CHANGE
  
  def to_right(self):
    if self.state != self.RUNNING_RIGHT:
      self.state = self.RUNNING_RIGHT
      self.frame_count = 0
      self.tick = self.TICK_CHANGE

  def to_idle(self):
    if self.state == self.RUNNING_RIGHT:
      self.state = self.IDLE_RIGHT
    else:
      self.state = self.IDLE_LEFT
    self.frame_count = 0
    self.tick = self.TICK_CHANGE
  
  def _adjust_position(self):
    y = self.rect.y
    if self.rect.left < 0:
      self.move_to(0, y)
    elif self.rect.right > co.SCREEN_WIDHT:
      self.move_to(co.SCREEN_WIDHT - self.rect.w, y)

  def update(self, *args, **kwargs):
    TICK_CHANGE = 6
    if self.state == self.IDLE_RIGHT:
      if self.tick == TICK_CHANGE:
        self.tick = 1
        self.image = self.idle_right_frames[self.frame_count]
        self.mask = self.idle_right_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.idle_right_frames)
    elif self.state == self.IDLE_LEFT:
      if self.tick == TICK_CHANGE:
        self.tick = 1
        self.image = self.idle_left_frames[self.frame_count]
        self.mask = self.idle_left_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.idle_left_frames)
    elif self.state == self.RUNNING_LEFT:
      if self.tick == TICK_CHANGE:
        self.tick = 1
        self.image = self.running_left_frames[self.frame_count]
        self.mask = self.running_left_masks[self.frame_count]
        self.frame_count = (self.frame_count + 1) % len(self.running_left_frames)
      self.rect.x -= self.speed
      self.magical_bar.rect.x -= self.speed
      self.magical_bar.angle_pointer.rect.x -= self.speed
      self._adjust_position()
    elif self.state == self.RUNNING_RIGHT:
      if self.tick == TICK_CHANGE:
        self.tick = 1
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
    BALL_DIM = 40
    # Loading frames
    # The size of the ball changes according to its strength.
    # Sice strength might be 1, 2 or 3, the ball might have 
    # three sizes and hence there are three sets of frames and 
    # three masks.
    original_frames = util.load_grid_images('assets/energy_ball_sheet.png', BALL_DIM, BALL_DIM, 5, 1)
    strong_frames = original_frames.copy()
    median_frames = [pygame.transform.scale_by(f, 0.6) for f in original_frames]
    weak_frames = [pygame.transform.scale_by(f, 0.3) for f in original_frames]
    strong_mask = pygame.mask.from_surface(strong_frames[0])
    median_mask = pygame.mask.from_surface(median_frames[0])
    weak_mask = pygame.mask.from_surface(weak_frames[0])
    self.dic_frames = {
      1: weak_frames, 
      2: median_frames, 
      3: strong_frames
    }
    self.dic_masks = {
      1: weak_mask, 
      2: median_mask, 
      3: strong_mask
    }
    # constants
    self.STANDARD_SPEED = 7
    self.ACCELERATED_SPEED = 1.8 * self.STANDARD_SPEED
    # initiating state
    self.frames = weak_frames
    self.image = self.frames[0]
    self.mask = weak_mask
    self.rect = self.image.get_rect()
    self.reset_movement()
    self.strength = 1
    self.change_speed_time = None
    # animation variables
    self.tick = 1
    self.frame_count = 1
  
  def increase_strength(self):
    if self.strength < 3:
      self.strength += 1
      self.frames = self.dic_frames[self.strength]
      self.mask = self.dic_masks[self.strength]
      self.rect.size = self.frames[0].get_rect().size
  
  def decrease_strength(self):
    if self.strength > 1:
      self.strength -= 1
      self.frames = self.dic_frames[self.strength]
      self.mask = self.dic_masks[self.strength]

  def reset_movement(self):
    self.speed = self.STANDARD_SPEED
    self.angle = math.pi / 2
    self.x_speed = self.speed * math.cos(self.angle)
    self.y_speed = self.speed * math.sin(self.angle) * -1

  def update(self, *args, **kwargs):
    # animation
    TICK_CHANGE_FRAME = 12
    if self.tick % TICK_CHANGE_FRAME == 0:
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    # speed control
    if (self.change_speed_time and 
        self.speed != self.STANDARD_SPEED and 
        pygame.time.get_ticks() - self.change_speed_time >= 800
      ):
      self.to_standard_speed()
    self.tick += 1
  
  def move(self, reboundig_sprites):
    '''
    This method moves the ball and adjusts its movement if it 
    collides with a sprite that generates a rebound, such as 
    blocks and enemies.

    :param reboundig_sprites: A sprite.Group containing the sprites able 
    to rebound the ball.
    '''
    # vertical movement
    self.rect.top += self.y_speed
    collided = pygame.sprite.spritecollide(self, reboundig_sprites, False)
    if collided:
      c = collided[0] # takes in account only one collision
      # TODO get the nearest sprite instead the first one
      if self.y_speed > 0: # Ball is moving down
        self.rect.bottom = c.rect.top - 1
      else: # Ball is moving up
        self.rect.top = c.rect.bottom + 1
      c.collide(self, co.VERTICAL_DIRECTION)
    
    # horizontal movement
    self.rect.left += self.x_speed
    collided = pygame.sprite.spritecollide(self, reboundig_sprites, False)
    if collided:
      c = collided[0] # takes in account only one collision
      if self.x_speed > 0: # Ball is moving right
        self.rect.right = c.rect.left - 1
      elif self.x_speed < 0: # Ball is moving left
        self.rect.left = c.rect.right + 1
      c.collide(self, co.HORIZONTAL_DIRECTION)
  
  def reverse_vertical_movement(self):
    self.y_speed *= -1
  
  def reverse_horizontal_movement(self):
    self.x_speed *= -1

  def to_down(self):
    if self.y_speed > 0:
      self.reverse_vertical_movement()
  
  def to_right(self):
    if self.x_speed < 0:
      self.reverse_horizontal_movement()
  
  def to_left(self):
    if self.x_speed > 0:
      self.reverse_horizontal_movement()

  def _change_speed(self, new_speed):
    if self.speed != new_speed:
      cos = self.x_speed / self.speed
      alpha = math.acos(cos)
      x_sense = self.x_speed / abs(self.x_speed)
      y_sense = self.y_speed / abs(self.y_speed)
      self.x_speed = new_speed * abs(math.cos(alpha)) * x_sense
      self.y_speed = new_speed * abs(math.sin(alpha)) * y_sense
      self.speed = new_speed
    self.change_speed_time = pygame.time.get_ticks()

  def accelerate(self):
    self._change_speed(self.ACCELERATED_SPEED)
  
  def to_standard_speed(self):
    self._change_speed(self.STANDARD_SPEED)

  def set_angle(self, new_angle):
    '''
    Sets the direction angle of the ball. This method was designed 
    to be called by the MagicalBar at the moment the ball collides 
    with it.
    '''
    self.x_speed = self.STANDARD_SPEED * math.cos(new_angle)
    self.y_speed = self.STANDARD_SPEED * math.sin(new_angle)
    self.speed = self.STANDARD_SPEED
    self.reverse_vertical_movement()
      
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
    thickness = 300
    self.left_boundary = Boundary(-thickness, 0, thickness, co.SCREEN_HEIGHT)
    self.right_boundary = Boundary(co.SCREEN_WIDHT + 1, 0, thickness, co.SCREEN_HEIGHT)
    self.top_boundary = Boundary(0, -thickness, co.SCREEN_WIDHT, thickness)
    self.boundaries = [self.left_boundary, self.right_boundary, self.top_boundary]
  
  def check_bump(self, ball):
    """
    Checks if the ball hitted any of the boundareis. In an positive 
    case, this function adjusts the position of the ball.
    """
    hitted_boundaries = pygame.sprite.spritecollide(ball, self.boundaries, False, pygame.sprite.collide_mask)
    if self.left_boundary in hitted_boundaries or self.right_boundary in hitted_boundaries:
      ball.reverse_horizontal_movement()
      if ball.x_speed > 0:
        ball.rect.left = 1
      else:
        ball.rect.right = co.SCREEN_WIDHT - 1
    if self.top_boundary in hitted_boundaries:
      ball.reverse_vertical_movement()
      ball.rect.top = self.top_boundary.rect.bottom + 1
    # Checking of the ball scaped through one of the upper corner
    if ball.rect.x <= 0 and ball.rect.y <= 0: # left corner
      ball.rect.topleft = (1, 1)
      ball.to_down()
      ball.to_right()
    elif ball.rect.x >= co.SCREEN_WIDHT and ball.rect.y <= 0: # right corner
      ball.rect.topright = (co.SCREEN_WIDHT - 1, 1)
      ball.to_down()
      ball.to_left()

  def below_screen(self, sprite):
    return sprite.rect.top > co.SCREEN_HEIGHT
  
class MagicalBar(pygame.sprite.Sprite):
  def __init__(self, angle_pointer):
    pygame.sprite.Sprite.__init__(self)
    FRAME_WIDTH = 90
    FRAME_HEIGHT = 7
    self.frames = util.load_grid_images('assets/magical_bar_sheet.png', FRAME_WIDTH, FRAME_HEIGHT, 4, 1)
    self.frames = [pygame.transform.scale(f, (co.PLAYER_FRAME_DIM, FRAME_HEIGHT)) for f in self.frames]
    self.masks = [pygame.mask.from_surface(img) for img in self.frames]
    self.image = self.frames[0]
    self.mask = self.masks[0]
    self.rect = self.image.get_rect()  
    self.tick = 1
    self.frame_count = 0
    self.angle_pointer = angle_pointer

  def update(self, *args, **kwargs):
    TICK_CHANGE = 12
    if self.tick == TICK_CHANGE:
      self.tick = 0
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    self.tick += 1
  
  def collide(self, ball):
    ball.rect.bottom = self.rect.top - 1
    ball.set_angle(self.angle_pointer.angle)

class AnglePointer(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = pygame.image.load('assets/angle_pointer.png').convert_alpha()
    self.image = self.original_image
    self.rect = self.image.get_rect()
    self.to_initial_angle()
    self.increase = False
    self.decrease = False
    self.update()

  def to_initial_angle(self):
    self.angle = math.pi / 2
    self.update_image()
  
  def update_image(self):
    rotated_img = pygame.transform.rotate(
      self.original_image, 
      math.degrees(self.angle - math.pi / 2)
    )
    # Get a new rect with the old center
    rotated_rect = rotated_img.get_rect(center=self.rect.center) 
    self.rect = rotated_rect
    self.image = rotated_img
  
  def update(self, *args, **kwargs):
    # angle update
    angle_step = math.pi / 8
    new_angle = None
    if self.increase:
      alpha = min(self.angle + angle_step, 3 * math.pi / 4)
      new_angle = alpha
    elif self.decrease:
      alpha = max(self.angle - angle_step, math.pi / 4)
      new_angle = alpha
    if new_angle:
      self.angle = new_angle
      self.update_image()
 
class InanimateProjectile(pygame.sprite.Sprite):
  def __init__(self, image_path, speed, centerx, top):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.speed = speed
    self.throwing_point = (centerx, top)
    self.hide()

  def throw(self):
    self.visible = True
    self.rect.midtop = self.throwing_point

  def hide(self):
    self.visible = False
    self.rect.topleft = (-self.rect.w - 5, -self.rect.h - 5)

  def update(self, *args, **kwargs):
    if self.visible:
      self.rect.y += self.speed
    if self.rect.y > co.SCREEN_HEIGHT:
      self.visible = False

class AmberBossGoblin(pygame.sprite.Sprite):
  def __init__(self, centerx, top):
    pygame.sprite.Sprite.__init__(self)
    self.idle_frames = util.load_grid_images(
      'assets/amber_goblin_idle_sheet.png', 
      co.AMBLER_GOBLIN_FRAME_DIM, co.AMBLER_GOBLIN_FRAME_DIM, 
      4, 1
    )
    self.idle_frames = [pygame.transform.scale_by(f, 2) for f in self.idle_frames]
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect()  
    self.mask = pygame.mask.from_surface(self.idle_frames[0])
    self.rect.midtop = (centerx, top)
    self.hit_points = 10
    self.tick = random.randint(0, 110)
    self.frame_count = random.randint(0, len(self.idle_frames) - 1)
    self.attack = util.create_big_dagger(self.rect.centerx, self.rect.bottom + 5)
    # red_idle_frames are used to indicate that the 
    # boss suffered a hit
    red_overlay = self.mask.to_surface(
      setcolor=(255, 0, 0, 50), 
      unsetcolor=(0, 0, 0, 0)
    )
    self.red_idle_frames = []
    for img in self.idle_frames:
      img = img.copy()
      img.blit(red_overlay, (0, 0))
      self.red_idle_frames.append(img)
    self.tick_hit = 0 # to control exibition of red_idle_frames

  def update(self, *args, **kwargs):
    TICK_ANIMATION = 6
    TICK_PROJECTILE = 120
    if self.tick % TICK_ANIMATION == 0:
      if self.tick_hit > 0:
        self.image = self.red_idle_frames[self.frame_count]
      else:
        self.image = self.idle_frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.idle_frames)
    if self.tick % TICK_PROJECTILE == 0:
      self.attack.throw()
    self.tick += 1
    self.tick_hit -= 1
  
  def collide(self, ball, direction):
    # this boss is imune to the weak boss
    if ball.strength > 1:
      self.image = self.red_idle_frames[self.frame_count]
      self.tick_hit = 10
      self.hit_points -= ball.strength
      if self.hit_points <= 0:
        self.kill()
    util.reverse_ball_direction(ball, direction)
    
class PurpleCrystal(pygame.sprite.Sprite):
  def __init__(self, topleft=None, midtop=None):
    pygame.sprite.Sprite.__init__(self)
    FRAME_DIM = 30
    self.frames = util.load_grid_images('assets/purple_crystal_sheet.png', FRAME_DIM, FRAME_DIM, 7, 1)
    self.image = self.frames[0]
    self.mask = pygame.mask.from_surface(self.frames[0])
    self.rect = self.image.get_rect()
    if topleft:
      self.rect.topleft = topleft
    if midtop:
      self.rect.midtop = midtop
    # animation
    self.tick = 1
    self.frame_count = 0

  def update(self, *args, **kwargs):
    # animation
    TICK_CHANGE = 12
    if self.tick == TICK_CHANGE:
      self.tick = 0
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    self.tick += 1
  
  def collide(self, sprites):
    for s in sprites:
      if isinstance (s, Ball):
        s.increase_strength()
        self.kill()
        return
      
class GreenCrystal(pygame.sprite.Sprite):
  def __init__(self, topleft=None, midtop=None):
    pygame.sprite.Sprite.__init__(self)
    FRAME_DIM = 30
    self.frames = util.load_grid_images('assets/green_crystal_sheet.png', FRAME_DIM, FRAME_DIM, 7, 1)
    self.image = self.frames[0]
    self.mask = pygame.mask.from_surface(self.frames[0])
    self.rect = self.image.get_rect()
    if topleft:
      self.rect.topleft = topleft
    if midtop:
      self.rect.midtop = midtop
    # animation
    self.tick = 1
    self.frame_count = 0

  def update(self, *args, **kwargs):
    # animation
    TICK_CHANGE = 12
    if self.tick == TICK_CHANGE:
      self.tick = 0
      self.image = self.frames[self.frame_count]
      self.frame_count = (self.frame_count + 1) % len(self.frames)
    self.tick += 1
  
  def collide(self, sprites):
    for s in sprites:
      if isinstance (s, Player):
        s.lives += 1
        self.kill()
        return