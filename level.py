import pygame, sys
import sprites, util

class Level:
  '''
  :param label: The number or name of the level.
  :param player: An instance of game.Game.
  :param enemies: A pygame.sprite.Group holding the level's enemies.
  :param blocks: A pygame.sprite.Group holding the level's blocks.
  :param power_ups: A pygame.sprite.Group holding the level's power ups.
  '''
  def __init__(self, label, game, enemies, blocks, power_ups):
    self.label = label
    self.game = game
    self.enemies = enemies
    self.blocks = blocks
    self.power_ups = power_ups

  def run(self):
    '''
    This method contains all the logic to run a level. 
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
    txt_level = font_stats.render(f"Level {self.label}", True, 'white')
    txt_victory = font_msgs.render("VICTORY!", True, '0x99369e')
    txt_continue = font_stats.render(f"Press ENTER to continue", True, '0x99369e')

    ## SPRITES ##
    arena = sprites.Arena()
    all_sprites = pygame.sprite.Group()
    # Player, pointer and bar
    player = self.game.player
    magical_bar = player.magical_bar
    angle_pointer = magical_bar.angle_pointer
    ball = sprites.Ball()
    all_sprites.add([player, ball, magical_bar, angle_pointer])
    util.center_player_and_ball(player, ball)
    # Enemies and attacks
    attacks = pygame.sprite.Group()
    for enemy in self.enemies:
      attack = enemy.attack
      all_sprites.add([enemy, attack])
      attacks.add(attack)
    enemy, attack = None, None
    # Blocks
    all_sprites.add(self.blocks)
    reboundig_sprites = self.blocks.copy()
    reboundig_sprites.add(self.enemies)
    # Power Ups
    if self.power_ups:
      all_sprites.add(self.power_ups)

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
        all_sprites.update()
        ball.move(reboundig_sprites) # manages collision with blocks and enemies
        arena.check_bump(ball)       # manages collision with screen boundaries
        # defeat conditions
        defeated = (
          arena.below_screen(ball) or 
          pygame.sprite.spritecollide(ball, [player], False, pygame.sprite.collide_mask) or # ball collided the player
          pygame.sprite.spritecollide(player, attacks, False, pygame.sprite.collide_mask)   # an attack collided the player
        )
        if defeated:
          player.lives -= 1
          if player.lives == 0:
            game_state = GAME_OVER
          else:
            game_state = LOST_LIFE
            lost_time = pygame.time.get_ticks()
        else:
          # collision between ball and magical bar
          if pygame.sprite.spritecollide(ball, [magical_bar], False, pygame.sprite.collide_mask):
            magical_bar.collide(ball)
          # collision among ball and power ups
          if self.power_ups:
            collided = pygame.sprite.spritecollide(ball, self.power_ups, False, pygame.sprite.collide_mask)
            for c in collided:
              c.collide(all_sprites)
          # checking victory
          if len(self.enemies) == 0:
            game_state = VICTORY      

      ### RENDERING ###
      self.game.screen.fill((0, 0, 0))
      self.game.draw_txt_level(txt_level)
      self.game.draw_txt_lives(txt_lives)
      all_sprites.draw(self.game.screen)
      if game_state == PAUSED:
        self.game.draw_msg(txt_paused)
      elif game_state == LOST_LIFE:
        self.game.draw_msg(txt_lost)
      elif game_state == GAME_OVER:
        self.game.draw_msg(txt_game_over)
        self.game.draw_msg(txt_continue, vertical_margin=30)
      elif game_state == ON_START:
        self.game.draw_msg(txt_start_1)
        self.game.draw_msg(txt_start_2, vertical_margin=30)
      elif game_state == VICTORY:
        self.game.draw_msg(txt_victory)
        self.game.draw_msg(txt_continue, vertical_margin=30)
      pygame.display.flip()
      self.game.clock.tick(45) # FPS
