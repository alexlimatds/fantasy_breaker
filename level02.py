import util, pygame, level
import sprites

def run(player):
  '''
  Defines the sprites of Level 02 and execute it
  
  :param player: An instance of sprites.Player.
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
  level.run(2, player, enemies, blocks)

def main():
  # Run this function to test the level
  angle_pointer = sprites.AnglePointer()
  magical_bar = sprites.MagicalBar(angle_pointer)
  player = sprites.Player(magical_bar, 3)
  run(player)

if __name__ == "__main__":
  main()