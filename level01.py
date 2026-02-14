import game, pygame, sys

def draw_msg(surface_txt, vertical_margin = 0):
  game.screen.blit(
    surface_txt, 
    (
      game.SCREEN_WIDHT / 2 - surface_txt.get_rect().w / 2, 
      game.SCREEN_HEIGHT / 2 - surface_txt.get_rect().h / 2 + vertical_margin
    )
  )

def run(player_lives):
  ## VARIABLES ##
  IN_GAME = 0
  PAUSED = 1
  LOST_LIFE = 2
  GAME_OVER = 3
  ON_START = 4
  game_state = ON_START
  start_count = 3

  ## TEXT ##
  font_msgs = pygame.font.Font(None, 40)
  font_stats = pygame.font.Font(None, 18)
  txt_paused = font_msgs.render("P A U S E", True, 'red')
  txt_game_over = font_msgs.render("GAME OVER", True, 'red')
  txt_lost = font_msgs.render("YOU HAVE LOST", True, 'red')

  ## SPRITES ##
  arena = game.Arena()
  player = game.Player(player_lives)
  ball = game.Ball()
  game.center_player_and_ball(player, ball)
  block = game.Block(10, 10)
  #t = player.rect.topleft
  #ball.rect.topleft = (t[0] + player.rect.width / 2, t[1] - 60)
  all_sprites = pygame.sprite.Group([player, block, ball])

  start_time = pygame.time.get_ticks()
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
    if game_state == ON_START:
      player.state = player.IDLE
      player.update()
      txt_start_1 = font_msgs.render('GET READY!', True, 'red')
      txt_start_2 = font_msgs.render(f'{start_count}', True, 'red')
      now = pygame.time.get_ticks()
      time_frame = now - start_time
      if time_frame >= 800:
        start_count -= 1
        start_time = now
      if start_count == 0:
        game_state = IN_GAME
    elif game_state == LOST_LIFE:
      now = pygame.time.get_ticks()
      time_frame = now - lost_time
      if time_frame >= 2000:
        lost_time = now
        game_state = ON_START
        start_count = 4
        game.center_player_and_ball(player, ball)
    elif game_state == IN_GAME:
      all_sprites.update()
      arena.check_bump(ball)
      collided = pygame.sprite.spritecollide(ball, [player], False, pygame.sprite.collide_mask)
      bellow_screen = arena.below_screen(ball)
      if collided or bellow_screen:
        if (player.state != player.AURA or bellow_screen) and player.lives == 1:
          player.lives = 0
          game_state = GAME_OVER
        elif (player.state != player.AURA or bellow_screen) and player.lives > 1:
          player.lives -= 1
          game_state = LOST_LIFE
          lost_time = pygame.time.get_ticks()

    ### RENDERING ###
    game.screen.fill((0, 0, 0))
    all_sprites.draw(game.screen)
    if game_state == PAUSED:
      draw_msg(txt_paused)
    elif game_state == LOST_LIFE:
      draw_msg(txt_lost)
    elif game_state == GAME_OVER:
      draw_msg(txt_game_over)
    elif game_state == ON_START:
      draw_msg(txt_start_1)
      draw_msg(txt_start_2, vertical_margin=30)
    pygame.display.flip()
    game.clock.tick(45) # FPS

def main():
  run(3)

if __name__ == "__main__":
  main()