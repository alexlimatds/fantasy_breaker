import game, pygame, sys

def run(player_lives):
  ## VARIABLES ##
  IN_GAME = 0
  PAUSED = 1
  LOST_LIFE = 2
  game_state = IN_GAME

  ## TEXT ##
  font_pause = pygame.font.Font(None, 24)
  txt_paused = font_pause.render("P A U S E", True, 'red')

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
        if game_state == IN_GAME:
          if event.key == pygame.K_LEFT:
            player.to_left()
          if event.key == pygame.K_RIGHT:
            player.to_right()
          if event.key == pygame.K_UP:
            player.to_aura()
      elif event.type == pygame.KEYUP:
        if (event.key == pygame.K_LEFT and player.state == player.RUNNING_LEFT) or \
           (event.key == pygame.K_RIGHT and player.state == player.RUNNING_RIGHT) or \
           (event.key == pygame.K_UP and player.state == player.AURA):
          player.to_idle()
        if game_state == IN_GAME:
          if event.key == pygame.K_p:
            game_state = PAUSED
        elif game_state == PAUSED:
          if event.key == pygame.K_p:
            game_state = IN_GAME

    ### GAME LOGIC ###
    if game_state == IN_GAME:
      all_sprites.update()
      arena.check_bump(ball)
      collided = pygame.sprite.spritecollide(ball, [player], False, pygame.sprite.collide_mask)
      if collided:
        pass

    ### RENDERING ###
    game.screen.fill((0, 0, 0))
    all_sprites.draw(game.screen)
    if game_state == PAUSED:
      game.screen.blit(
        txt_paused, 
        (game.SCREEN_WIDHT / 2 - txt_paused.get_rect().w / 2, game.SCREEN_HEIGHT / 2 - txt_paused.get_rect().h / 2))
    pygame.display.flip()
    game.clock.tick(45) # FPS

def main():
  run(3)


if __name__ == "__main__":
  main()