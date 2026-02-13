import game, pygame, sys

def run(player_lives):
  ## VARIABLES ##
  in_game = True

  ## SPRITES ##
  arena = game.Arena()
  player = game.Player(player_lives)
  block = game.Block(10, 10)
  ball = game.Ball()
  t = player.rect.topleft
  ball.rect.topleft = (t[0] + player.rect.width / 2, t[1] - 60)
  all_sprites = pygame.sprite.Group([player, block, ball])

  while True:
    ### INPUT ###
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    if in_game:
      pressed_keys = pygame.key.get_pressed()
      if pressed_keys[pygame.K_LEFT]:
        player.move_left()
      if pressed_keys[pygame.K_RIGHT]:
        player.move_right()

    ### GAME LOGIC ###
    all_sprites.update()
    arena.check_bump(ball)

    ### RENDERING ###
    game.screen.fill((0, 0, 0))
    all_sprites.draw(game.screen)
    pygame.display.flip()
    game.clock.tick(45) # FPS

def main():
  run(3)


if __name__ == "__main__":
  main()