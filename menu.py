import pygame

# Определение размеров окна
WIDTH, HEIGHT = 1200, 800

# Установка частоты кадров в секунду
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()

# Создание объекта окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Загрузка изображения фона меню
mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

# Загрузка логотипа
logo_img = pygame.image.load('images/capital2050.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

# Создание прямоугольников для кнопок
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

# Флаг для отображения меню
show_menu = True

while show_menu:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Выход из игры, если нажата кнопка "Закрыть"
            show_menu = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если была нажата кнопка мыши
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                # Если нажата кнопка "Начать игру", запускаем игру из game.py
                show_menu = False
                import game
                game.main()
                break
            elif quit_button_rect.collidepoint(x, y):
                # Если нажата кнопка "Выйти из игры", выходим из игры
                show_menu = False
                break


    # Отрисовка элементов
    screen.blit(mainmenu_img, (0, 0))

     # Отрисовка логотипа
    screen.blit(logo_img, (logo_x, logo_y))

    # Отрисовка кнопок
    font = pygame.font.Font(None, 32)
    text = font.render("Начать игру", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
        # Если курсор находится над кнопкой, подсвечиваем ее красным
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    screen.blit(text, (play_button_rect.x + 35, play_button_rect.y + 10))

    text = font.render("Выйти из игры", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
        # Если курсор находится над кнопкой, подсвечиваем ее красным
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    screen.blit(text, (quit_button_rect.x + 25, quit_button_rect.y + 10))

    # Обновление экрана
    pygame.display.flip()

    # Контроль частоты кадров
    clock.tick(60)

# Выход из Pygame
pygame.quit()
