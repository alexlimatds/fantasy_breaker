import game, pygame

# This unit is aimed only to code testing
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
dim = 115
imgs = game.load_grid_images('assets/player_run_right_sheet.png', dim, dim, 8, 1)
idx = 0
for i in range(2):
  for j in range(3):
    x = 20 + dim * j
    y = 20 + dim * i
    screen.blit(imgs[idx], (x, y))
    pygame.draw.rect(screen, 'white', pygame.Rect(x, y, dim, dim), width=2)
    idx += 1

pygame.display.flip() # Desenha o quadro atual na tela

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  clock.tick(45)
