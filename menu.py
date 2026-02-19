import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
from settings import game_settings


def animate_screen():
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25 if game_settings.get("music_enabled") else 0)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25 if game_settings.get("sfx_enabled") else 0)

if game_settings.get("fullscreen"):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

BUTTON_WIDTH = 205
BUTTON_HEIGHT = 50
BUTTON_SPACING = 25

play_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 75, BUTTON_WIDTH, BUTTON_HEIGHT)
settings_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
quit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 75, BUTTON_WIDTH, BUTTON_HEIGHT)

pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25 if game_settings.get("sfx_enabled") else 0)
selected_button = 0
show_menu = True
in_settings = False
in_high_scores = False

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


def draw_button(surface, rect, text, is_selected, font):
    pygame.draw.rect(surface, BLACK, rect, border_radius=10)
    if is_selected:
        pygame.draw.rect(surface, RED, rect, border_radius=10, width=4)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def draw_toggle_button(surface, rect, label, value, is_selected, font):
    pygame.draw.rect(surface, BLACK, rect, border_radius=10)
    if is_selected:
        pygame.draw.rect(surface, RED, rect, border_radius=10, width=4)
    status = "ON" if value else "OFF"
    color = (100, 255, 100) if value else (255, 100, 100)
    text_surface = font.render(f"{label}: ", True, WHITE)
    status_surface = font.render(status, True, color)
    total_width = text_surface.get_width() + status_surface.get_width()
    start_x = rect.centerx - total_width // 2
    surface.blit(text_surface, (start_x, rect.centery - text_surface.get_height() // 2))
    surface.blit(status_surface, (start_x + text_surface.get_width(), rect.centery - status_surface.get_height() // 2))


def draw_value_button(surface, rect, label, value, is_selected, font):
    pygame.draw.rect(surface, BLACK, rect, border_radius=10)
    if is_selected:
        pygame.draw.rect(surface, RED, rect, border_radius=10, width=4)
    text_surface = font.render(f"{label}: {value.upper()}", True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def show_settings_menu():
    global in_settings, selected_button, screen
    
    settings_options = ["music", "sfx", "fullscreen", "difficulty", "high_scores", "back"]
    selected_setting = 0
    
    SETTINGS_BUTTON_WIDTH = 320
    settings_rects = []
    start_y = HEIGHT // 2 - 150
    for i in range(len(settings_options)):
        rect = pygame.Rect(
            WIDTH // 2 - SETTINGS_BUTTON_WIDTH // 2,
            start_y + i * 60,
            SETTINGS_BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        settings_rects.append(rect)
    
    font = pygame.font.SysFont('Comic Sans MS', 30)
    title_font = pygame.font.SysFont('Comic Sans MS', 50)
    
    while in_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_settings = False
                elif event.key == pygame.K_UP:
                    selected_setting = (selected_setting - 1) % len(settings_options)
                elif event.key == pygame.K_DOWN:
                    selected_setting = (selected_setting + 1) % len(settings_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    handle_settings_action(settings_options[selected_setting])
                    if settings_options[selected_setting] == "back":
                        in_settings = False
                    elif settings_options[selected_setting] == "fullscreen":
                        if game_settings.get("fullscreen"):
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, rect in enumerate(settings_rects):
                    if rect.collidepoint(x, y):
                        handle_settings_action(settings_options[i])
                        if settings_options[i] == "back":
                            in_settings = False
                        elif settings_options[i] == "fullscreen":
                            if game_settings.get("fullscreen"):
                                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            else:
                                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                for i, rect in enumerate(settings_rects):
                    if rect.collidepoint(x, y):
                        selected_setting = i
            
            if joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        handle_settings_action(settings_options[selected_setting])
                        if settings_options[selected_setting] == "back":
                            in_settings = False
                        elif settings_options[selected_setting] == "fullscreen":
                            if game_settings.get("fullscreen"):
                                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            else:
                                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif event.button == 1:
                        in_settings = False
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[1] == 1:
                        selected_setting = (selected_setting - 1) % len(settings_options)
                    elif event.value[1] == -1:
                        selected_setting = (selected_setting + 1) % len(settings_options)
        
        screen.blit(mainmenu_img, (0, 0))
        
        title = title_font.render("SETTINGS", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        for i, option in enumerate(settings_options):
            is_selected = (i == selected_setting)
            if option == "music":
                draw_toggle_button(screen, settings_rects[i], "Music", game_settings.get("music_enabled"), is_selected, font)
            elif option == "sfx":
                draw_toggle_button(screen, settings_rects[i], "Sound Effects", game_settings.get("sfx_enabled"), is_selected, font)
            elif option == "fullscreen":
                draw_toggle_button(screen, settings_rects[i], "Fullscreen", game_settings.get("fullscreen"), is_selected, font)
            elif option == "difficulty":
                draw_value_button(screen, settings_rects[i], "Difficulty", game_settings.get("difficulty"), is_selected, font)
            elif option == "high_scores":
                draw_button(screen, settings_rects[i], "High Scores", is_selected, font)
            elif option == "back":
                draw_button(screen, settings_rects[i], "Back", is_selected, font)
        
        pygame.display.flip()
        clock.tick(60)


def handle_settings_action(option):
    global in_high_scores
    
    if option == "music":
        game_settings.toggle("music_enabled")
        if game_settings.get("music_enabled"):
            pygame.mixer.music.set_volume(game_settings.get("music_volume"))
        else:
            pygame.mixer.music.set_volume(0)
    elif option == "sfx":
        game_settings.toggle("sfx_enabled")
        vol = game_settings.get_sfx_volume()
        for i in range(pygame.mixer.get_num_channels()):
            try:
                channel = pygame.mixer.Channel(i)
                channel.set_volume(vol)
            except:
                pass
        explosion_sound.set_volume(vol)
    elif option == "fullscreen":
        game_settings.toggle("fullscreen")
    elif option == "difficulty":
        game_settings.cycle_difficulty()
    elif option == "high_scores":
        show_high_scores_screen()


def show_high_scores_screen():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    title_font = pygame.font.SysFont('Comic Sans MS', 50)
    small_font = pygame.font.SysFont('Comic Sans MS', 24)
    
    back_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
            if joystick and event.type == pygame.JOYBUTTONDOWN:
                running = False
        
        screen.blit(mainmenu_img, (0, 0))
        
        title = title_font.render("HIGH SCORES", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        scores = game_settings.get_high_scores()
        
        if not scores:
            no_scores = font.render("No high scores yet!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(no_scores, no_scores_rect)
        else:
            start_y = 160
            for i, entry in enumerate(scores):
                rank_color = (255, 215, 0) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50) if i == 2 else WHITE
                rank_text = f"{i + 1}."
                name_text = entry.get("name", "Player")[:12]
                score_text = str(entry.get("score", 0))
                
                rank_surface = font.render(rank_text, True, rank_color)
                name_surface = font.render(name_text, True, WHITE)
                score_surface = font.render(score_text, True, (255, 255, 100))
                
                y_pos = start_y + i * 45
                screen.blit(rank_surface, (WIDTH // 2 - 200, y_pos))
                screen.blit(name_surface, (WIDTH // 2 - 140, y_pos))
                screen.blit(score_surface, (WIDTH // 2 + 100, y_pos))
        
        draw_button(screen, back_rect, "Back", True, font)
        
        pygame.display.flip()
        clock.tick(60)


while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                game_settings.play_sound(explosion_sound)
                animate_screen()
                show_menu = False
                import main
                main.main()
                break
            elif settings_button_rect.collidepoint(x, y):
                in_settings = True
                show_settings_menu()
            elif quit_button_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                selected_button = 0
            elif settings_button_rect.collidepoint(x, y):
                selected_button = 1
            elif quit_button_rect.collidepoint(x, y):
                selected_button = 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = (selected_button - 1) % 3
            elif event.key == pygame.K_DOWN:
                selected_button = (selected_button + 1) % 3
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    game_settings.play_sound(explosion_sound)
                    animate_screen()
                    show_menu = False
                    screen.fill(BLACK)
                    import main
                    main.main()
                    break
                elif selected_button == 1:
                    in_settings = True
                    show_settings_menu()
                elif selected_button == 2:
                    pygame.quit()
                    sys.exit()

        if joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_button == 0:
                        game_settings.play_sound(explosion_sound)
                        animate_screen()
                        show_menu = False
                        screen.fill(BLACK)
                        import main
                        main.main()
                        break
                    elif selected_button == 1:
                        in_settings = True
                        show_settings_menu()
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    selected_button = (selected_button - 1) % 3
                elif event.value[1] == -1:
                    selected_button = (selected_button + 1) % 3

    screen.blit(mainmenu_img, (0, 0))
    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.SysFont('Comic Sans MS', 40)
    draw_button(screen, play_button_rect, "Play", selected_button == 0, font)
    draw_button(screen, settings_button_rect, "Settings", selected_button == 1, font)
    draw_button(screen, quit_button_rect, "Exit", selected_button == 2, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
