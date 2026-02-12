import game, pygame, sys

def run():
  player = game.Player()
  block = game.Block(10, 10)
  
  all_sprites = pygame.sprite.Group([player, block])

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    ### GAME LOGIC ###


    ### RENDERING ###
    game.screen.fill((0, 0, 0))
    all_sprites.draw(game.screen)
    pygame.display.flip()
    game.clock.tick(45) # FPS

def main():
  run()


if __name__ == "__main__":
  main()