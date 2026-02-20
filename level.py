import game, pygame, sys
import constants as co
import sprites, util

def run(level, player, enemies, blocks, power_ups=None):
  '''
  This function contains all the logic to run a level. 
  
  :param level: The number or name of the level.
  :param player: An instance of sprites.Player.
  :param enemies: A pygame.sprite.Group holding the level's enemies.
  :param blocks: A pygame.sprite.Group holding the level's blocks.
  :param power_ups: A pygame.sprite.Group holding the level's power ups.
  '''
  ## VARIABLES ##
  IN_GAME = 0
  PAUSED = 1
  LOST_LIFE = 2
  GAME_OVER = 3
  ON_START = 4
  VICTORY = 5
  game_state = ON_START
  start_count = 3
  run_game_loop = True

  ## TEXT ##
  font_msgs = pygame.font.Font(None, 40)
  font_stats = pygame.font.Font(None, 20)
  txt_paused = font_msgs.render("P A U S E", True, 'red')
  txt_game_over = font_msgs.render("GAME OVER", True, 'red')
  txt_lost = font_msgs.render("DEFEAT", True, 'red')
  txt_level = font_stats.render(f"Level {level}", True, 'white')
  txt_victory = font_msgs.render("VICTORY!", True, '0x99369e')
  txt_continue = font_stats.render(f"Press ENTER to continue", True, '0x99369e')

  ## SPRITES ##
  all_sprites = pygame.sprite.Group()
  arena = sprites.Arena()
  magical_bar = player.magical_bar
  angle_pointer = magical_bar.angle_pointer
  ball = sprites.Ball()
  all_sprites.add([player, ball, magical_bar, angle_pointer])
  util.center_player_and_ball(player, ball)
  attacks = pygame.sprite.Group()
  for enemy in enemies:
    attack = enemy.attack
    all_sprites.add([enemy, attack])
    attacks.add(attack)
  enemy, attack = None, None
  all_sprites.add(blocks)
  targets = blocks.copy()
  targets.add(enemies)
  if power_ups:
    all_sprites.add(power_ups)

  ## GAME LOOP ##
  start_time = pygame.time.get_ticks()
  while run_game_loop:
    ### INPUT ###
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if game_state == IN_GAME:
          if event.key == pygame.K_UP:
            angle_pointer.increase = True
          if event.key == pygame.K_DOWN:
            angle_pointer.decrease = True
      elif event.type == pygame.KEYUP:
        if (event.key == pygame.K_LEFT and player.state == player.RUNNING_LEFT) or \
           (event.key == pygame.K_RIGHT and player.state == player.RUNNING_RIGHT):
          player.to_idle()
        if game_state == IN_GAME:
          if event.key == pygame.K_p:
            game_state = PAUSED
        elif game_state == PAUSED:
          if event.key == pygame.K_p:
            game_state = IN_GAME
        elif game_state == VICTORY or game_state == GAME_OVER:
          if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
            run_game_loop = False
        if event.key == pygame.K_UP:
          angle_pointer.increase = False
        if event.key == pygame.K_DOWN:
          angle_pointer.decrease = False
      player.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      player.to_left()
    if keys[pygame.K_RIGHT]:
      player.to_right()
      
    ### GAME LOGIC ###
    txt_lives = font_stats.render(f"Lives: {player.lives}", True, 'white')
    if game_state == ON_START:
      for a in attacks:
        a.hide()
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
        util.center_player_and_ball(player, ball)
        player.to_initial_stance()
        player.update()
    elif game_state == IN_GAME:
      arena.check_bump(ball)
      defeated = False
      # collision between ball and player
      collided = pygame.sprite.spritecollide(ball, [player], False, pygame.sprite.collide_mask)
      bellow_screen = arena.below_screen(ball)
      if collided or bellow_screen:
        defeated = True
      # collision between ball and magical bar
      collided = pygame.sprite.spritecollide(ball, [magical_bar], False, pygame.sprite.collide_mask)
      if collided:
        magical_bar.collide(ball)
      # collision among player and attacks
      collided = pygame.sprite.spritecollide(player, attacks, False, pygame.sprite.collide_mask)
      if collided:
        defeated = True
      # collision among ball and blocks
      collided = pygame.sprite.spritecollide(ball, blocks, False, pygame.sprite.collide_mask)
      for c in collided:
        c.collide(ball)
      # collision among ball and enemies
      collided = pygame.sprite.spritecollide(ball, enemies, False, pygame.sprite.collide_mask)
      for c in collided:
        c.collide(ball)
      # collision among ball and power ups
      if not power_ups:
        power_ups = []
      collided = pygame.sprite.spritecollide(ball, power_ups, False, pygame.sprite.collide_mask)
      for c in collided:
        c.collide(all_sprites)
      if len(enemies) == 0:
        game_state = VICTORY
      # checking defeat
      if defeated and player.lives == 1:
        player.lives = 0
        game_state = GAME_OVER
      elif defeated and player.lives > 1:
        player.lives -= 1
        game_state = LOST_LIFE
        lost_time = pygame.time.get_ticks()
      all_sprites.update(target_sprites=targets)

    ### RENDERING ###
    game.screen.fill((0, 0, 0))
    game.draw_txt_level(txt_level)
    game.draw_txt_lives(txt_lives)
    all_sprites.draw(game.screen)
    if game_state == PAUSED:
      game.draw_msg(txt_paused)
    elif game_state == LOST_LIFE:
      game.draw_msg(txt_lost)
    elif game_state == GAME_OVER:
      game.draw_msg(txt_game_over)
      game.draw_msg(txt_continue, vertical_margin=30)
    elif game_state == ON_START:
      game.draw_msg(txt_start_1)
      game.draw_msg(txt_start_2, vertical_margin=30)
    elif game_state == VICTORY:
      game.draw_msg(txt_victory)
      game.draw_msg(txt_continue, vertical_margin=30)
    pygame.display.flip()
    game.clock.tick(45) # FPS
