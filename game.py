import pygame, sprites
import constants as co

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

# Icons by Lorc: https://lorcblog.blogspot.com/
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://luizmelo.itch.io/monsters-creatures-fantasy
# https://beast-pixels.itch.io/crafting-materials
# https://petraheim.itch.io/breakout-pixelart

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

def draw_msg(surface_txt, vertical_margin = 0):
  screen.blit(
    surface_txt, 
    (
      co.SCREEN_WIDHT / 2 - surface_txt.get_rect().w / 2, 
      co.SCREEN_HEIGHT / 2 - surface_txt.get_rect().h / 2 + vertical_margin
    )
  )

def draw_txt_level(surface_txt):
  screen.blit(surface_txt, (5, 5))

def draw_txt_lives(surface_txt):
  screen.blit(
    surface_txt, 
    (
      co.SCREEN_WIDHT - surface_txt.get_rect().w - 5, 
      5
    )
  )

def create_dagger(center_x, y):
  dg = sprites.InanimateProjectile(
    'assets/dagger.png', 
    5, 
    center_x, 
    y
  )
  return dg

def create_amber_goblin(center_x, top):
  goblin = sprites.AmberGoblin(center_x, top)
  dagger = goblin.attack
  return goblin, dagger

### INITIALIZATION ###
pygame.init()
screen = pygame.display.set_mode((co.SCREEN_WIDHT, co.SCREEN_HEIGHT))
pygame.display.set_caption("Fantasy Breaker")
clock = pygame.time.Clock()