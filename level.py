import pygame, sys
import sprites, util, assets
import constants as co

def generate_text(font, msg, color, shadow=False):
  txt = font.render(msg, True, color)
  if shadow:
    sh = font.render(msg, True, 'black')
    offset = sh.get_rect().h * 0.08
    sh.blit(sh, (offset, offset))
    sh.blit(txt, (0, 0))
    return sh
  else:
    return txt
  
class Level:
  '''
  :param label: A text describing the level.
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
    ## DRAWING AREAS ##
    self.area_info_bg_color = '0x3d3d42'
    self.area_info = pygame.Surface((
      co.SCREEN_WIDHT, 
      co.INFO_BAR_HEIGHT
    ))
    self.area_info.fill(self.area_info_bg_color)

    self.area_game = pygame.Surface((
      co.SCREEN_WIDHT, 
      co.GAME_AREA_HEIGHT
    ))
    self.area_game.fill((0, 0, 0))
    ## IMAGES ##
    self.hourglass_img = pygame.transform.scale_by(assets.HOURGLASS_IMG, 0.8)
    self.bar_extender_img = assets.BAR_EXTENDER_SHEET[0]
    ## FONTS ##
    self.font_msgs = pygame.font.Font('assets/alagard.ttf', 40)
    self.font_stats = pygame.font.Font('assets/LGGothic.ttf', 20)
  
  def draw_msg(self, surface_txt, vertical_margin = 0):
    self.area_game.blit(
      surface_txt, 
      (
        co.SCREEN_WIDHT / 2 - surface_txt.get_rect().w / 2, 
        co.SCREEN_HEIGHT / 2 - surface_txt.get_rect().h / 2 + vertical_margin
      )
    )

  def draw_info_area(self):
    # Level label
    self.area_info.blit(self.txt_level, (5, 5))
    # Player's lives
    self.area_info.blit(
      self.txt_lives, 
      (
        co.SCREEN_WIDHT - self.txt_lives.get_rect().w - 5, 
        5
      )
    )
    # Ball decelerator power-up
    x = 130
    self.area_info.blit(self.hourglass_img, (x, 3))
    txt = generate_text(self.font_stats, f'Z: {self.game.player.ball_decelerator}', 'white')
    x += 30
    self.area_info.blit(txt, (x, 5))
    # Bar extender power up
    x += 50
    self.area_info.blit(self.bar_extender_img, (x, 0))
    txt = generate_text(self.font_stats, f'X: {self.game.player.bar_extender}', 'white')
    x += 45
    self.area_info.blit(txt, (x, 5))


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
    txt_paused = generate_text(self.font_msgs, 'P A U S E', 'red', True)
    txt_game_over = generate_text(self.font_msgs, 'GAME OVER', 'red', True)
    txt_lost = generate_text(self.font_msgs, 'DEFEAT', 'red', True)
    self.txt_level = generate_text(self.font_stats, f"{self.label}", 'white')
    txt_victory = generate_text(self.font_msgs, 'VICTORY!', '0x99369e', True)
    txt_continue = generate_text(self.font_stats, 'Press ENTER to continue', '0x99369e', True)

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
    rebounding_sprites = self.blocks.copy()
    rebounding_sprites.add(self.enemies)
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
              angle_pointer.increase_angle()
            if event.key == pygame.K_DOWN:
              angle_pointer.decrease_angle()
            if event.key == pygame.K_z:
              player.slow_down_ball(ball)
            if event.key == pygame.K_x:
              player.enlarge_bar()
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
          if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            angle_pointer.stop_angle_change()
        player.update()

      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
        player.to_left()
      if keys[pygame.K_RIGHT]:
        player.to_right()
        
      ### GAME LOGIC ###
      self.txt_lives = generate_text(self.font_stats, f"Lives: {player.lives}", 'white')
      if game_state == ON_START:
        for a in attacks:
          a.hide()
        txt_start_1 = generate_text(self.font_msgs, 'GET READY!', 'red', True)
        txt_start_2 = generate_text(self.font_msgs, f'{start_count}', 'red', True)
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
        ball.move(rebounding_sprites) # manages collision with blocks and enemies
        arena.check_bump(ball)        # manages collision with screen boundaries
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
      self.area_info.fill(self.area_info_bg_color)
      self.area_game.fill((0, 0, 0))
      self.draw_info_area()
      all_sprites.draw(self.area_game)
      if game_state == PAUSED:
        self.draw_msg(txt_paused)
      elif game_state == LOST_LIFE:
        self.draw_msg(txt_lost)
      elif game_state == GAME_OVER:
        self.draw_msg(txt_game_over)
        self.draw_msg(txt_continue, vertical_margin=30)
      elif game_state == ON_START:
        self.draw_msg(txt_start_1)
        self.draw_msg(txt_start_2, vertical_margin=30)
      elif game_state == VICTORY:
        self.draw_msg(txt_victory)
        self.draw_msg(txt_continue, vertical_margin=30)
      self.game.screen.blit(self.area_info, (0, 0))
      self.game.screen.blit(self.area_game, (0, self.area_info.get_rect().h))

      pygame.display.flip()
      self.game.clock.tick(45) # FPS

def build_level(label, sprites_matrix, game):
  # max lines -> 11
  # max columns -> 16
  enemies = pygame.sprite.Group()
  blocks = pygame.sprite.Group()
  power_ups = pygame.sprite.Group()

  max_i = (co.GAME_AREA_HEIGHT - 2 * co.PLAYER_FRAME_DIM) // co.BLOCK_HEIGHT
  max_j = co.SCREEN_WIDHT // co.BLOCK_WIDTH
  for i, line in enumerate(sprites_matrix):
    if i + 1 > max_i:
        raise ValueError(f'Matrix with more than {max_i} lines')
    top_y = i * co.BLOCK_HEIGHT + 30
    for j, symbol in enumerate(line):
      if j + 1 > max_j:
        raise ValueError(f'Matrix with more than {max_j} columns')
      center_x = j * co.BLOCK_WIDTH + co.BLOCK_WIDTH / 2
      if symbol == 'CB':
        blocks.add(sprites.ConcreteBlock(center_x, top_y))
      elif symbol == 'BB':
        blocks.add(sprites.BrickBlock(center_x, top_y))
      elif symbol == 'EB':
        blocks.add(sprites.EnergyBlock(center_x, top_y))
      elif symbol == 'BLB':
        blocks.add(sprites.BloodBLock(center_x, top_y))
      elif symbol == 'AB':
        enemies.add(sprites.AmberGoblin(center_x, top_y))
      elif symbol == 'ABG':
        enemies.add(sprites.AmberBossGoblin(center_x, top_y))
      elif symbol == 'PC':
        power_ups.add(sprites.PurpleCrystal(midtop=(center_x, top_y)))
      elif symbol == 'GC':
        power_ups.add(sprites.GreenCrystal(midtop=(center_x, top_y)))
      elif symbol == 'HG':
        power_ups.add(sprites.Hourglass(midtop=(center_x, top_y)))
      elif symbol == 'BE':
        power_ups.add(sprites.BarExtender(midtop=(center_x, top_y)))
  
  return Level(label, game, enemies, blocks, power_ups)
