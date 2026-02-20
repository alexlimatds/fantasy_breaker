import util, pygame, level, sprites

def run(game):
  '''
  Defines the sprites of Level 02 and execute it
  
  :param game: An instance of game.Game
  '''
  ## SPRITES ##
  enemies = pygame.sprite.Group()
  y = 30
  enemy, _ = util.create_amber_goblin(230, y)
  enemies.add(enemy)
  enemy, _ = util.create_amber_goblin(570, y)
  enemies.add(enemy)
  y = 200
  for i in range(150, 800, 250):
    enemy, _ = util.create_amber_goblin(i, y)
    enemies.add(enemy)
  enemy = None
  
  blocks = pygame.sprite.Group()
  y = 100
  for i in range(0, 13):
    b = sprites.BrickBlock(0, y)
    b.rect.left = i * 62
    blocks.add(b)
  ## RUN LEVEL ##
  level.run(2, game, enemies, blocks)
