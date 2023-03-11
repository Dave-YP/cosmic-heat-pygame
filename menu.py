import pygame

WIDTH, HEIGHT = 1200, 800

FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/capital2050.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)


show_menu = True

while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show_menu = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                show_menu = False
                import game
                game.main()
                break
            elif quit_button_rect.collidepoint(x, y):
                show_menu = False
                break


    screen.blit(mainmenu_img, (0, 0))

    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.Font(None, 32)
    text = font.render("Начать игру", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    screen.blit(text, (play_button_rect.x + 35, play_button_rect.y + 10))

    text = font.render("Выйти из игры", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    screen.blit(text, (quit_button_rect.x + 25, quit_button_rect.y + 10))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
