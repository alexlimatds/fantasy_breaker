import util, pygame, level, sprites
import constants as co

def run(game):
  '''
  Defines the sprites of Level 02 and execute it
  
  :param game: An instance of game.Game
  '''
  ## SPRITES ##
  enemies = pygame.sprite.Group()
  y = 175
  x = 300
  for i in range(1, 4):
    enemy, _ = util.create_amber_goblin(x, y)
    enemies.add(enemy)
    x += 100
  enemy = None
  
  blocks = pygame.sprite.Group()
  v1 = co.SCREEN_WIDHT / 2
  v2 = 3
  blocks.add(sprites.ConcreteBlock(v1, v2))
  for i in range(1, 5):
    x1 = v1 - i * 45
    y = (v2 + 32) * i
    blocks.add(sprites.ConcreteBlock(x1, y))
    x2 = v1 + i * 45
    blocks.add(sprites.ConcreteBlock(x2, y))
  for i in range(5, 7):
    y = (v2 + 32) * i
    blocks.add(sprites.BrickBlock(x1, y))
    blocks.add(sprites.BrickBlock(x2, y))
  y = (v2 + 32) * 7
  for i in range(0, 7):
    x = x1 + 58 * i + 3
    blocks.add(sprites.ConcreteBlock(x, y))

  b = None
  ## RUN LEVEL ##
  level.run(3, game, enemies, blocks)
