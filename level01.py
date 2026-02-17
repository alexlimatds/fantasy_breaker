import game, pygame, level
import constants as co
import sprites

def run(player):
  '''
  Defines the sprites of Level 01 and execute it
  
  :param player: An instance of sprites.Player.
  '''
  ## SPRITES ##
  enemies = pygame.sprite.Group()
  for i in range(100, 800, 200):
    enemy, _ = game.create_amber_goblin(i, 30)
    enemies.add(enemy)
  enemy = None
  blocks = pygame.sprite.Group()
  ## RUN LEVEL ##
  level.run(1, player, enemies, blocks)

def main():
  # Run this function to test the level
  angle_pointer = sprites.AnglePointer()
  magical_bar = sprites.MagicalBar(angle_pointer)
  player = sprites.Player(magical_bar, 3)
  run(player)

if __name__ == "__main__":
  main()