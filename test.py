# Определение цветов
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Отображение кнопок в главном меню
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
button_color = GRAY
exit_color = GRAY

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            # Выбрана кнопка "Начать игру"
            if button_rect.collidepoint(x, y):
                show_mainmenu = False

            # Выбрана кнопка "Выход"
            elif exit_button_rect.collidepoint(x, y):
                exit_game()
        
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos

            # Реакция на наведение на кнопку "Начать игру"
            if button_rect.collidepoint(x, y):
                button_color = RED
            else:
                button_color = GRAY
            
            # Реакция на наведение на кнопку "Выход"
            if exit_button_rect.collidepoint(x, y):
                exit_color = RED
            else:
                exit_color = GRAY
    
    # Отрисовка элементов
    if show_mainmenu:
        screen.blit(mainmenu_img, (0, 0))
        font = pygame.font.Font(None, 40)
        
        # Отображение кнопки "Начать игру"
        button_surface = pygame.Surface(button_rect.size)
        button_surface.fill(button_color)
        screen.blit(button_surface, button_rect)
        text = font.render("Начать игру", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 15))
        
        # Отображение кнопки "Выход"
        exit_surface = pygame.Surface(exit_button_rect.size)
        exit_surface.fill(exit_color)
        screen.blit(exit_surface, exit_button_rect)
        exit_text = font.render("Выход", True, WHITE)
        screen.blit(exit_text, (WIDTH // 2 - 35, HEIGHT // 2 + 60))
    else:
        # Отображение игровых объектов
        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, WHITE, player_rect)
    
    # Обновление экрана
    pygame.display.flip()

    # Контроль частоты кадров
    clock.tick(FPS)

# Выход из игры, остановка звука
pygame.mixer.music.stop()
pygame.quit()
