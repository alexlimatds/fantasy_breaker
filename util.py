import pygame
import sprites as sp
import constants as co

def load_grid_images(sheet_file, width, height, columns, rows):
  '''
  Load frames/tiles from a sprite sheet.
  
  :param sheet: path of sheet file
  :param width: frame's width
  :param height: frame's height
  :param columns: number of columns in the sheet
  :param rows: number of rows in the sheet
  '''
  sheet_image = pygame.image.load(sheet_file).convert_alpha()
  images = []
  cell_width = sheet_image.get_rect().w / columns
  cell_height = sheet_image.get_rect().h / rows
  x_delta = (cell_width - width) / 2
  y_delta = (cell_height - height) / 2
  for row in range(rows):
    for col in range(columns):
      x = col * cell_width + x_delta
      y = row * cell_height + y_delta
      img = pygame.Surface([width, height], pygame.SRCALPHA)
      img.blit(sheet_image, (0, 0), (x, y, width, height))
      images.append(img)
  return images

def center_player_and_ball(player, ball):
  player.move_to(
    co.SCREEN_WIDHT / 2 - player.rect.w / 2, 
    co.SCREEN_HEIGHT - player.rect.h - 5
  )
  t = player.rect.topleft
  ball.rect.topleft = (
    t[0] + player.rect.width / 2 + 5, 
    t[1] - 60
  )
  ball.reset_movement()

def create_dagger(center_x, y):
  dg = sp.InanimateProjectile(
    'assets/dagger.png', 
    5, 
    center_x, 
    y
  )
  return dg

def create_big_dagger(center_x, y):
  dg = sp.InanimateProjectile(
    'assets/dagger.png', 
    10, 
    center_x, 
    y
  )
  dg.image = pygame.transform.scale_by(dg.image, 2)
  dg.rect = dg.image.get_rect()
  return dg

def create_amber_goblin(center_x, top):
  goblin = sp.AmberGoblin(center_x, top)
  dagger = goblin.attack
  return goblin, dagger

def create_amber_boss_goblin(center_x, top):
  goblin = sp.AmberBossGoblin(center_x, top)
  dagger = goblin.attack
  return goblin, dagger