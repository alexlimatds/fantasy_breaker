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
      elif event.type == pygame.KEYDOWN:
        if in_game:
          if event.key == pygame.K_LEFT:
            player.to_left()
          if event.key == pygame.K_RIGHT:
            player.to_right()
          if event.key == pygame.K_UP:
            player.to_aura()
      elif event.type == pygame.KEYUP:
        if in_game:
          if (event.key == pygame.K_LEFT and player.state == player.RUNNING_LEFT) or \
             (event.key == pygame.K_RIGHT and player.state == player.RUNNING_RIGHT) or \
             (event.key == pygame.K_UP and player.state == player.AURA):
            player.to_idle()

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