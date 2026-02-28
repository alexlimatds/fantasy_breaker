import pygame, util
import constants as co
import level01, level02, level03, level04

# https://opengameart.org/content/700-rpg-icons
# https://opengameart.org/content/dungeon-crawl-32x32-tiles
# https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental
# https://opengameart.org/content/roguelike-tiles-large-collection

# Icons by Lorc: https://lorcblog.blogspot.com/
# https://beast-pixels.itch.io/crafting-materials

# https://luizmelo.itch.io/monsters-creatures-fantasy
# Alagard font by Hewett Tsoi (https://www.dafont.com/alagard.font)
# Romulus font by Hewett Tsoi (https://www.dafont.com/romulus.font)
# LG Gothic font by Molnár Benedek (https://www.dafont.com/lggothic.font)

class Game:
  def __init__(self):
    ### INITIALIZATION ###
    pygame.init()
    self.screen = pygame.display.set_mode((co.SCREEN_WIDHT, co.SCREEN_HEIGHT))
    pygame.display.set_caption("Fantasy Breaker")
    self.clock = pygame.time.Clock()
  
  def start(self):
    levels = [level01.run, level02.run, level03.run, level04.run]
    self.player = util.create_player(3)
    for f in levels:
      f(self)
      if self.player.lives <= 0:
        # game over
        break
    

def main():
  Game().start()

if __name__ == "__main__":
  main()