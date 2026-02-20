import game, pygame, level
import constants as co
import sprites

def run(player):
  '''
  Defines the sprites of Level 04 and execute it
  
  :param player: An instance of sprites.Player.
  '''
  ## SPRITES ##
  enemies = pygame.sprite.Group()
  blocks = pygame.sprite.Group()
  y = 15
  enemy = sprites.AmberBossGoblin(co.SCREEN_WIDHT / 2, y)
  enemies.add(enemy)
  
  y += enemy.rect.h + 15
  x = 1
  block = sprites.BrickBlock(0, y)
  block.rect.left = x
  blocks.add(block)
  block_w = block.rect.w
  block_h = block.rect.h
  for i in range(3):
    x += (block_w + 5)
    block = sprites.ConcreteBlock(0, y)
    blocks.add(block)
    block.rect.left = x
  
  x = co.SCREEN_WIDHT - block_w - 1
  block = sprites.BrickBlock(0, y)
  block.rect.left = x
  blocks.add(block)
  for i in range(3):
    x -= (block_w + 5)
    block = sprites.ConcreteBlock(0, y)
    blocks.add(block)
    block.rect.left = x
  
  for i in range(3):
    y += block_h + 5
    block = sprites.BrickBlock(0, y)
    blocks.add(block)
    block.rect.x = 1
    block = sprites.BrickBlock(0, y)
    blocks.add(block)
    block.rect.x = co.SCREEN_WIDHT - block_w - 1

  y += 10
  x = co.SCREEN_WIDHT / 2 - 200
  enemy = game.create_amber_goblin(x, y)[0]
  enemies.add(enemy)
  x += 400
  enemies.add(game.create_amber_goblin(x, y)[0])
  
  y += enemy.rect.h + 10
  x = co.SCREEN_WIDHT / 2
  blocks.add(sprites.ConcreteBlock(x, y))
  x -= 200
  blocks.add(sprites.BrickBlock(x, y))
  x += 400
  blocks.add(sprites.BrickBlock(x, y))

  y = 24
  x1 = 1 + block_w + 5
  x2 = co.SCREEN_WIDHT - (1 + block_w + 5) * 2
  block = sprites.BrickBlock(0, y)
  block.rect.left = x1
  blocks.add(block)
  
  block = sprites.BrickBlock(0, y)
  block.rect.left = x2
  blocks.add(block)

  power_ups = pygame.sprite.Group()
  power_ups.add(sprites.PurpleCrystal((10, y + 20)))
  power_ups.add(sprites.GreenCrystal((co.SCREEN_WIDHT - 40, y + 20)))

  y += block_h + 10
  block = sprites.BrickBlock(0, y)
  block.rect.left = x1
  blocks.add(block)
  
  block = sprites.BrickBlock(0, y)
  block.rect.left = x2
  blocks.add(block)

  enemy = None
  block = None
  ## RUN LEVEL ##
  level.run(4, player, enemies, blocks, power_ups=power_ups)

def main():
  # Run this function to test the level
  angle_pointer = sprites.AnglePointer()
  magical_bar = sprites.MagicalBar(angle_pointer)
  player = sprites.Player(magical_bar, 3)
  run(player)

if __name__ == "__main__":
  main()