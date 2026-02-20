import util, pygame, level, sprites
import game as gm

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
  level.run(1, game, enemies, blocks)

def main():
  # Run this function to test the level
  game = gm.Game()
  game.player = util.create_player(3)
  run(game)

if __name__ == "__main__":
  main()