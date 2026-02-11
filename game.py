import pygame

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

### CONSTANTS ###
W_WIDHT = 600
W_HEIGHT = 600

BLOCK_WIDHT = 50
BLOCK_HEIGHT = 20

class Block(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([BLOCK_WIDHT, BLOCK_HEIGHT])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)
    self.hit_points = 1

class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([50, 10])
    self.image.fill((0, 255, 255))
    self.rect = self.image.get_rect()  
    self.rect.topleft = (
      W_WIDHT / 2 - BLOCK_WIDHT / 2, 
      W_HEIGHT - BLOCK_HEIGHT - 10
    )
    self.lives = 3

pygame.init()
screen = pygame.display.set_mode((W_WIDHT, W_HEIGHT))
pygame.display.set_caption("Fantasy Breaker")

clock = pygame.time.Clock()