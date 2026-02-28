import util, pygame, sprites
import level as lv

def run(game):
  '''
  Defines the sprites of Level 01 and execute it
  
  :param game: An instance of game.Game
  '''
  ## SPRITES ##
  enemies = pygame.sprite.Group()
  y = 30
  for i in range(100, 800, 200):
    enemy, _ = util.create_amber_goblin(i, y)
    enemies.add(enemy)
  enemy = None
  blocks = pygame.sprite.Group()
  for i in range(100, 800, 200):
    blocks.add(sprites.BrickBlock(i - 40, y + 100))
    blocks.add(sprites.BrickBlock(i + 40, y + 100))
  ## RUN LEVEL ##
  level = lv.Level("Level 1", game, enemies, blocks, None)
  level.run()
