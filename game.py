import pygame

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

# Icons by Lorc: https://lorcblog.blogspot.com/

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
    self.image = pygame.Surface([50, 10])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (
      SCREEN_WIDHT / 2 - BLOCK_WIDHT / 2, 
      SCREEN_HEIGHT - BLOCK_HEIGHT - 10
    )
    self.lives = lives

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    img = pygame.image.load('assets/mace-head.png').convert_alpha()
    self.image = pygame.transform.scale(img, (BALL_SIZE, BALL_SIZE))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)

class Arena:
  # This class is used to check if an sprite reaches the edges of the screen
  def __init__(self):
    self.left_edge = pygame.Rect(-1, 0, 1, SCREEN_HEIGHT)
  
  def hit_edge(self, sprite):
    pass
    


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