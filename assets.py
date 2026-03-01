import util, pygame
import constants as co


HOURGLASS_IMG = None
BAR_EXTENDER_SHEET = None

def init():
  global HOURGLASS_IMG, BAR_EXTENDER_SHEET
  HOURGLASS_IMG = pygame.image.load('assets/hourglass.png').convert_alpha()
  BAR_EXTENDER_SHEET = util.load_grid_images(
    'assets/bar_extender_sheet.png', 40, 30, 5, 1
)
