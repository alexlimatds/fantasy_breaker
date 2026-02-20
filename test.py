import game, pygame, level
import constants as co
import sprites

def run(player):
  '''
  Defines the sprites of Level 01 and execute it
  
  :param player: An instance of sprites.Player.
  '''
  ## SPRITES ##
  e = sprites.AmberBossGoblin(co.SCREEN_WIDHT / 2 - 40, 15)
  enemies = pygame.sprite.Group(e)
  x = 500
  blocks = pygame.sprite.Group()
  for i in range(1, 7):
    b = sprites.ConcreteBlock(x + i * 55, 300)
    b.hit_points = 1000
    blocks.add(b)
  
  power_ups = pygame.sprite.Group(
    sprites.GreenCrystal(
      (co.SCREEN_WIDHT/2 + 60, 200)
      )
    )
  ## RUN LEVEL ##
  level.run('Test', player, enemies, blocks, power_ups=power_ups)

def main():
  # Run this function to test the level
  angle_pointer = sprites.AnglePointer()
  magical_bar = sprites.MagicalBar(angle_pointer)
  player = sprites.Player(magical_bar, 3)
  run(player)

if __name__ == "__main__":
  main()