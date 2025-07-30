import pygame
from game import Game, add_score
from ui import Button, create_gradient, title_letter_separation, title_animation
from sound import SoundManager


FULL_HD_RESOLUTION = (1920, 1080)
TITLE_SCREEN_STATE = 1
SINGLEPLAYER_SCREEN_STATE = 2
MULTIPLAYER_SCREEN_STATE = 3
OPTIONS_SCREEN_STATE = 4
TUTORIAL_SCREEN_STATE = 5
GAME_STATE = TITLE_SCREEN_STATE
flags = pygame.RESIZABLE

pygame.init()
screen = pygame.display.set_mode(FULL_HD_RESOLUTION)
clock = pygame.time.Clock()

game = Game(620, 400, 30, 4)
soundManager = SoundManager()
soundManager.play_music()

singleplayer_button = Button(860, 550, 200, 60, "Singleplayer")
multiplayer_button = Button(860, 630, 200, 60, "Multiplayer")
options_button = Button(860, 710, 200, 60, "Options")
tutorial_button = Button(860, 780, 200, 60, "How to play")
quit_button = Button(860, 860, 200, 60, "Quit")

pygame.display.set_caption("Kameňožrút")
icon = pygame.image.load("../assets/images/rocks.png")
title_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", 100)
ui_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", 40)
pygame.display.set_icon(icon)

score = 0
score_text = ui_font.render("Score:", 1, (255, 255, 255))
score_value = ui_font.render(str(score), 1, (255, 255, 255))

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
                GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                game.initialize_grid()
                # game.update_grid(board)
            if multiplayer_button.is_clicked(event):
                GAME_STATE = MULTIPLAYER_SCREEN_STATE
            if options_button.is_clicked(event):
                GAME_STATE = OPTIONS_SCREEN_STATE
                print("Options")
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
                                # board = game.update_grid(updated_board)

                        # game.update_grid(result["grid"])
        # if quit_button.is_clicked(event):
        #     game.send_quit_button_press(game_id)
    if GAME_STATE is TITLE_SCREEN_STATE:
        title_animation(FULL_HD_RESOLUTION, letters, elapsed_time)
        for letter in letters:
            screen.blit(letter['surface'], letter['rect'])
        singleplayer_button.draw(screen)
        multiplayer_button.draw(screen)
        options_button.draw(screen)
        tutorial_button.draw(screen)
    elif GAME_STATE is SINGLEPLAYER_SCREEN_STATE:
        screen.blit(score_text, (260, 870))
        screen.blit(score_value, (410, 870))

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

    quit_button.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
