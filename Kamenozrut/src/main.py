import pygame
from game import Game, add_score
from ui import Button, create_gradient, title_letter_separation, title_animation
from sound import SoundManager
from db import (set_score, get_max_score, set_musiclevel, get_musiclevel, set_soundlevel, get_soundlevel,
                set_colorscheme, get_colorscheme)


FULL_HD_RESOLUTION = (1920, 1080)
TITLE_SCREEN_STATE = 1
SINGLEPLAYER_SCREEN_STATE = 2
MULTIPLAYER_SCREEN_STATE = 3
OPTIONS_SCREEN_STATE = 4
TUTORIAL_SCREEN_STATE = 5
SINGLEPLAYER_MODE_SELECTION_STATE = 6
GAME_STATE = TITLE_SCREEN_STATE
flags = pygame.RESIZABLE

pygame.init()
screen = pygame.display.set_mode(FULL_HD_RESOLUTION)
clock = pygame.time.Clock()

game = Game(620, 300, 30, 4)
soundManager = SoundManager()
soundManager.play_music()

singleplayer_button = Button(860, 580, 200, 60, "Singleplayer")
multiplayer_button = Button(860, 650, 200, 60, "Multiplayer")
options_button = Button(860, 720, 200, 60, "Options")
tutorial_button = Button(860, 790, 200, 60, "How to play")
quit_button = Button(860, 860, 200, 60, "Quit")
back_button = Button(860, 790, 200, 60, "Back to the main menu")
standard_singleplayer_mode_button = Button(860, 470, 200, 60, "Standard mode")
color_madness_singleplayer_mode_button = Button(860, 550, 200, 60, "Color madness mode")

music_up_button = Button(990, 200, 60, 60, "+")
music_down_button = Button(870, 200, 60, 60, "-")
sound_up_button = Button(990, 300, 60, 60, "+")
sound_down_button = Button(870, 300, 60, 60, "-")
color_scheme_1 = Button(670, 550, 200, 60, "Color Chaos")
color_scheme_2 = Button(1050, 550, 200, 60, "Passionate Papaya")
color_scheme_3 = Button(670, 680, 200, 60, "Boring Brick")
color_scheme_4 = Button(1050, 680, 200, 60, "Lush Lagoon")

pygame.display.set_caption("Kameňožrút")
icon = pygame.image.load("../assets/images/rocks.png")
title_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", 100)
ui_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", 40)
pygame.display.set_icon(icon)

all_colors = [[(49, 86, 89), (65, 211, 189), (186, 50, 79), (255, 186, 73), (255, 169, 231), (254, 225, 199)], # color chaos
              [(114, 17, 33), (165, 64, 45), (241, 81, 86), (249, 160, 63), (255, 192, 127), (255, 207, 153),], # passionate papaya
              [(70, 63, 58), (8, 3, 87), (138, 129, 124), (188, 184, 177), (244, 243, 238), (224, 175, 160)], # boring brick
              [(4, 42, 43), (55, 39, 114), (116, 124, 146), (148, 197, 149), (161, 232, 175), (253, 236, 239)]] # lush lagoon

music_level_value = get_musiclevel()
soundManager.set_music_volume(music_level_value)
music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
music_level_value_rect = music_level_value_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 310))

music_level_text = ui_font.render("Music level", 1, (255, 255, 255))
music_level_rect = music_level_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 350))

sound_level_value = get_soundlevel()
soundManager.set_sound_volume(sound_level_value)
sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
sound_level_value_rect = sound_level_value_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 210))

sound_level_text = ui_font.render("Sound level", 1, (255, 255, 255))
sound_level_rect = sound_level_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 250))

default_scheme = get_colorscheme()
color_scheme = ui_font.render("Choose a color scheme:", 1, (255, 255, 255))
color_scheme_rect = color_scheme.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 30))

score = 0
score_text = ui_font.render("Score:", 1, (255, 255, 255))
score_value = ui_font.render(str(score), 1, (255, 255, 255))

high_score = get_max_score()
high_score_text = ui_font.render("High Score:", 1, (255, 255, 255))
high_score_value = ui_font.render(str(high_score), 1, (255, 255, 255))

win_text = title_font.render("You WON!", 1, (255, 255, 255))
win_text_rect = win_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2))
game_over_message = ""

letters = title_letter_separation(FULL_HD_RESOLUTION, title_font)

background = create_gradient(FULL_HD_RESOLUTION)
running = True
elapsed_time = 0
while running:
    delta_time = clock.tick(60) / 1000.0  # Čas v sekundách
    elapsed_time += delta_time

    screen.blit(background, (0, 0))
    # TODO treba to nejako sprehľadniť - je tu chaos v tom kóde
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if quit_button.is_clicked(event):
            running = False
        if GAME_STATE == TITLE_SCREEN_STATE:
            if singleplayer_button.is_clicked(event):
                GAME_STATE = SINGLEPLAYER_MODE_SELECTION_STATE
            if multiplayer_button.is_clicked(event):
                GAME_STATE = MULTIPLAYER_SCREEN_STATE
            if options_button.is_clicked(event):
                color_scheme_grid = game.initialize_color_scheme_squares(all_colors)
                GAME_STATE = OPTIONS_SCREEN_STATE
            if tutorial_button.is_clicked(event):
                GAME_STATE = TUTORIAL_SCREEN_STATE
                print("Tutorial")

        elif GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, row in enumerate(game.grid):
                    for j, cell in enumerate(row):
                        if cell is not None:
                            rect, color = cell
                            if rect.collidepoint(pos):
                                connected_squares_len = game.handle_move(i, j, color)
                                score += add_score(connected_squares_len)
                                score_value = ui_font.render(str(score), 1, (255, 255, 255))
                                game_over_message = game.is_game_over()
                                if game_over_message == "You won":
                                    set_score(score)

            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
        elif GAME_STATE == SINGLEPLAYER_MODE_SELECTION_STATE:
            if standard_singleplayer_mode_button.is_clicked(event):
                game.colors = all_colors[default_scheme][:4]
                game.initialize_grid()
                GAME_STATE = SINGLEPLAYER_SCREEN_STATE
            if color_madness_singleplayer_mode_button.is_clicked(event):
                game.colors = all_colors[default_scheme]
                game.initialize_grid()
                GAME_STATE = SINGLEPLAYER_SCREEN_STATE
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
        elif GAME_STATE == MULTIPLAYER_SCREEN_STATE:
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
        elif GAME_STATE == OPTIONS_SCREEN_STATE:
            if music_up_button.is_clicked(event):
                if music_level_value < 10:
                    music_level_value += 1
                    soundManager.set_music_volume(music_level_value)
                    music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
                    set_musiclevel(music_level_value)
            if music_down_button.is_clicked(event):
                if music_level_value > 0:
                    music_level_value -= 1
                    soundManager.set_music_volume(music_level_value)
                    music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
                    set_musiclevel(music_level_value)
            if sound_up_button.is_clicked(event):
                if sound_level_value < 10:
                    sound_level_value += 1
                    soundManager.set_sound_volume(sound_level_value)
                    sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
                    set_soundlevel(sound_level_value)
            if sound_down_button.is_clicked(event):
                if sound_level_value > 0:
                    sound_level_value -= 1
                    soundManager.set_sound_volume(sound_level_value)
                    sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
                    set_soundlevel(sound_level_value)
            if color_scheme_1.is_clicked(event):
                default_scheme = 0
                set_colorscheme(default_scheme)
            if color_scheme_2.is_clicked(event):
                default_scheme = 1
                set_colorscheme(default_scheme)
            if color_scheme_3.is_clicked(event):
                default_scheme = 2
                set_colorscheme(default_scheme)
            if color_scheme_4.is_clicked(event):
                default_scheme = 3
                set_colorscheme(default_scheme)
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
        elif GAME_STATE == TUTORIAL_SCREEN_STATE:
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE

    if GAME_STATE == TITLE_SCREEN_STATE:
        title_animation(FULL_HD_RESOLUTION, letters, elapsed_time)
        for letter in letters:
            screen.blit(letter['surface'], letter['rect'])
        singleplayer_button.draw(screen)
        multiplayer_button.draw(screen)
        options_button.draw(screen)
        tutorial_button.draw(screen)
    elif GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
        screen.blit(high_score_text, (260, 830))
        screen.blit(high_score_value, (520, 830))
        screen.blit(score_text, (260, 870))
        screen.blit(score_value, (410, 870))
        back_button.draw(screen)
        if game_over_message == "You won":
            screen.blit(win_text, win_text_rect)

        pos = pygame.mouse.get_pos()
        for i, row in enumerate(game.grid):
            for j, cell in enumerate(row):
                if cell is not None:
                    rect, color = cell
                    if rect.collidepoint(pos):
                        connected_squares = game.find_connected_squares(i, j, color)
                        if len(connected_squares) > 1:
                            game.highlight_connected_squares(connected_squares, screen)
        game.draw(screen)
    elif GAME_STATE == SINGLEPLAYER_MODE_SELECTION_STATE:
        standard_singleplayer_mode_button.draw(screen)
        color_madness_singleplayer_mode_button.draw(screen)
        back_button.draw(screen)
    elif GAME_STATE == MULTIPLAYER_SCREEN_STATE:
        back_button.draw(screen)
    elif GAME_STATE == OPTIONS_SCREEN_STATE:
        screen.blit(music_level_text, music_level_rect)
        screen.blit(music_level_value_text, music_level_value_rect)
        music_up_button.draw(screen)
        music_down_button.draw(screen)
        screen.blit(sound_level_text, sound_level_rect)
        screen.blit(sound_level_value_text, sound_level_value_rect)
        sound_up_button.draw(screen)
        sound_down_button.draw(screen)
        screen.blit(color_scheme, color_scheme_rect)
        color_scheme_1.draw(screen)
        color_scheme_2.draw(screen)
        color_scheme_3.draw(screen)
        color_scheme_4.draw(screen)
        back_button.draw(screen)
        game.draw_color_scheme_selection(screen, color_scheme_grid)
        if default_scheme == 0:
            pygame.draw.line(screen, (0, 0, 0), (660, 660), (880, 660), 5)
        elif default_scheme == 1:
            pygame.draw.line(screen, (0, 0, 0), (1040, 660), (1260, 660), 5)
        elif default_scheme == 2:
            pygame.draw.line(screen, (0, 0, 0), (660, 790), (880, 790), 5)
        elif default_scheme == 3:
            pygame.draw.line(screen, (0, 0, 0), (1040, 790), (1260, 790), 5)
    elif GAME_STATE == TUTORIAL_SCREEN_STATE:
        back_button.draw(screen)

    quit_button.draw(screen)
    pygame.display.flip()

pygame.quit()
