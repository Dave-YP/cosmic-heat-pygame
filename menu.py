import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
from display import init_display, get_display


def animate_screen(screen, mainmenu_img, display):
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        display.present()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        display.present()
        pygame.time.wait(10)


pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

# Initialize the shared display manager
menu_display = init_display()
screen = menu_display.get_game_surface()

pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25)
selected_button = 0
show_menu = True

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            menu_display.handle_resize(event.w, event.h)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                menu_display.toggle_fullscreen()
            elif event.key == pygame.K_ESCAPE:
                if menu_display.is_fullscreen():
                    menu_display.toggle_fullscreen()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Convert window coordinates to logical coordinates
            logical_x, logical_y = menu_display.window_to_logical(*event.pos)
            if play_button_rect.collidepoint(logical_x, logical_y):
                explosion_sound.play()
                animate_screen(screen, mainmenu_img, menu_display)
                show_menu = False
                import main
                main.main()
                break
            elif quit_button_rect.collidepoint(logical_x, logical_y):
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = 0
            elif event.key == pygame.K_DOWN:
                selected_button = 1
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    explosion_sound.play()
                    animate_screen(screen, mainmenu_img, menu_display)
                    show_menu = False
                    screen.fill(BLACK)
                    import main
                    main.main()
                    break
                elif selected_button == 1:
                    pygame.quit()
                    sys.exit()

        if joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen(screen, mainmenu_img, menu_display)
                        show_menu = False
                        screen.fill(BLACK)
                        import main
                        main.main()
                        break
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    selected_button = 0
                elif event.value[1] == -1:
                    selected_button = 1

    screen.blit(mainmenu_img, (0, 0))

    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)
    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)

    menu_display.present()
    clock.tick(60)

pygame.quit()