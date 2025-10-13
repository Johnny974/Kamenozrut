import pygame
from game import Game, add_score
from ui import (Button, create_gradient, animate_title, create_title, FONT_SIZE, TITLE_FONT_SIZE, SMALL_FONT_SIZE)
from sound import SoundManager
from db import (set_score, get_max_score, set_musiclevel, get_musiclevel, set_soundlevel, get_soundlevel,
                set_colorscheme, get_colorscheme, update_score)
from client import check_internet_connection, connect_to_server, send_message, is_valid_nickname, is_in_match

FULL_HD_RESOLUTION = (1920, 1080)
TITLE_SCREEN_STATE = 1
SINGLEPLAYER_SCREEN_STATE = 2
MULTIPLAYER_SCREEN_STATE = 3
OPTIONS_SCREEN_STATE = 4
TUTORIAL_SCREEN_STATE = 5
SINGLEPLAYER_MODE_SELECTION_STATE = 6
GAME_STATE = TITLE_SCREEN_STATE


PREVIOUS_GAME_STATE = 0
CURRENT_GAME_MODE = ""
is_nickname_set = False
flags = pygame.RESIZABLE

pygame.init()
screen = pygame.display.set_mode(FULL_HD_RESOLUTION)
clock = pygame.time.Clock()

game = Game(620, 300, 30, 4)
sound_manager = SoundManager()
sound_manager.play_music()


# TODO should i move these buttons and texts to a different file?
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

new_game_button = Button(860, 120, 200, 60, "New game")
join_lobby_button = Button(860, 630, 200, 60, "Join the lobby")
find_match_button = Button(860, 550, 200, 60, "Play")

pygame.display.set_caption("Kameňožrút")
icon = pygame.image.load("../assets/images/rocks.png")
title_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", TITLE_FONT_SIZE)
ui_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", FONT_SIZE)
small_ui_font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", SMALL_FONT_SIZE)
pygame.display.set_icon(icon)

all_colors = [[(65, 211, 189), (186, 50, 79), (255, 186, 73), (255, 169, 231), (254, 225, 199)],  # color chaos
              [(114, 17, 33), (165, 64, 45), (241, 81, 86), (249, 160, 63), (255, 207, 153),],  # passionate papaya
              [(241, 81, 82), (255, 125, 0), (255, 236, 209), (21, 97, 109), (0, 21, 36)],  # boring brick
              [(177, 24, 200), (223, 253, 255), (144, 190, 222), (104, 237, 198), (144, 243, 255)]]  # lush lagoon

music_level_value = get_musiclevel()
sound_manager.set_music_volume(music_level_value)
music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
music_level_value_rect = music_level_value_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2,
                                                                 FULL_HD_RESOLUTION[1] // 2 - 310))

music_level_text = ui_font.render("Music level", 1, (255, 255, 255))
music_level_rect = music_level_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 350))

sound_level_value = get_soundlevel()
sound_manager.set_sound_volume(sound_level_value)
sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
sound_level_value_rect = sound_level_value_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2,
                                                                 FULL_HD_RESOLUTION[1] // 2 - 210))

sound_level_text = ui_font.render("Sound level", 1, (255, 255, 255))
sound_level_rect = sound_level_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 250))

default_scheme = get_colorscheme()
color_scheme = ui_font.render("Choose a color scheme:", 1, (255, 255, 255))
color_scheme_rect = color_scheme.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2 - 30))

tutorial_text_1 = ui_font.render("1. Your goal is to remove all the stones on the board.",
                                 1, (255, 255, 255))
tutorial_text_1_rect = tutorial_text_1.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 160))

tutorial_text_2 = ui_font.render("2. You can only destroy group of adjacent stones of the same color.",
                                 1, (255, 255, 255))
tutorial_text_2_rect = tutorial_text_2.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 240))

tutorial_text_3 = ui_font.render("3. If there is a gap in a column, the stones will drop down.",
                                 1, (255, 255, 255))
tutorial_text_3_rect = tutorial_text_3.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 320))

tutorial_text_4 = ui_font.render("4. If you win, your score is written into a database.",
                                 1, (255, 255, 255))
tutorial_text_4_rect = tutorial_text_4.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 400))

tutorial_text_5 = ui_font.render("5. After winning, you can add up to your score in the next game!",
                                 1, (255, 255, 255))
tutorial_text_5_rect = tutorial_text_5.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 480))

tutorial_text_6 = ui_font.render("Good luck and have fun!", 1, (255, 255, 255))
tutorial_text_6_rect = tutorial_text_6.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, 660))

won_any_game = False
score = 0
score_text = ui_font.render("Score:", 1, (255, 255, 255))
score_value = ui_font.render(str(score), 1, (255, 255, 255))

enemy_score = 0
enemy_score_text = ui_font.render("Opponent's Score:", 1, (255, 255, 255))
enemy_score_value = ui_font.render(str(enemy_score), 1, (255, 255, 255))

high_score = 0
high_score_text = ui_font.render("High Score:", 1, (255, 255, 255))
high_score_value = ui_font.render(str(high_score), 1, (255, 255, 255))

win_text = title_font.render("You WON!", 1, (255, 255, 255))
win_text_rect = win_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2))
game_over_message = ""

lose_text = title_font.render("You LOST!", 1, (255, 255, 255))
lose_text_rect = win_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2))


enter_nickname_text = ui_font.render("Enter your nickname:", 1, (255, 255, 255))
enter_nickname_text_rect = enter_nickname_text.get_rect(center=(FULL_HD_RESOLUTION[0] // 2, FULL_HD_RESOLUTION[1] // 2))
multiplayer_nickname = ""
multiplayer_nickname_text_box = pygame.Rect(730, FULL_HD_RESOLUTION[1] // 2 + 30, 100, 50)
active_nickname_text_box = False

multiplayer_error = "Connecting to the server..."
multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
multiplayer_error_text_rect = multiplayer_error_text.get_rect(topleft=(200, 940))

opponents_name = None
opponents_board = Game(1388, 300, 30, 4)

title = create_title(FULL_HD_RESOLUTION, title_font)


def show_error(message, opponent=None, opponents_grid=None, opponents_color_scheme=None, square_description=None):
    global multiplayer_error, multiplayer_error_text, opponents_name, enemy_score, enemy_score_value
    multiplayer_error = message
    multiplayer_error_text = small_ui_font.render(multiplayer_error, True, (255, 255, 255))
    if opponent:
        opponents_name = opponent
        serialized_grid = mp_game.serialize_grid()
        current_color_scheme = get_colorscheme()
        send_message(sock, "GRID", {"nickname": multiplayer_nickname, "grid": serialized_grid, "color_scheme": current_color_scheme})
    if opponents_grid:
        deserialized_opponents_grid = opponents_board.deserialize_grid(opponents_grid)
        opponents_board.grid = deserialized_opponents_grid
        opponents_board.colors = opponents_color_scheme
        # print(f"Here is board and color scheme of your opponent: {opponents_board.grid}, {opponents_board.colors}")
    if square_description:
        opponents_squares_len = opponents_board.handle_move(square_description[0], square_description[1], square_description[2])
        enemy_score += add_score(opponents_squares_len)
        enemy_score_value = ui_font.render(str(enemy_score), 1, (255, 255, 255))
        # square_description = None


background = create_gradient(FULL_HD_RESOLUTION)
running = True
elapsed_time = 0
while running:
    delta_time = clock.tick(60) / 1000.0  # Čas v sekundách
    elapsed_time += delta_time

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == sound_manager.MUSIC_END_EVENT:
        #     pygame.time.set_timer(sound_manager.MUSIC_DELAY_EVENT, 30000, loops=1)
        # if event.type == sound_manager.MUSIC_DELAY_EVENT:
        #     sound_manager.play_music()
        if quit_button.is_clicked(event):
            sound_manager.play_sound("click")
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
                    color_scheme_grid = game.initialize_color_scheme_squares(all_colors)
                    GAME_STATE = OPTIONS_SCREEN_STATE
                    PREVIOUS_GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                elif GAME_STATE == OPTIONS_SCREEN_STATE:
                    GAME_STATE = PREVIOUS_GAME_STATE
                elif GAME_STATE == MULTIPLAYER_SCREEN_STATE:
                    GAME_STATE = OPTIONS_SCREEN_STATE
                    color_scheme_grid = mp_game.initialize_color_scheme_squares(all_colors)
                    PREVIOUS_GAME_STATE = MULTIPLAYER_SCREEN_STATE
            if GAME_STATE == MULTIPLAYER_SCREEN_STATE:
                if active_nickname_text_box:
                    if event.key == pygame.K_BACKSPACE:
                        multiplayer_nickname = multiplayer_nickname[:-1]
                    elif len(multiplayer_nickname) == 15:
                        print("Sorry, too long nickname")
                    else:
                        multiplayer_nickname += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if multiplayer_nickname_text_box.collidepoint(event.pos):
                active_nickname_text_box = True
            else:
                active_nickname_text_box = False
        if GAME_STATE == TITLE_SCREEN_STATE:
            if singleplayer_button.is_clicked(event):
                GAME_STATE = SINGLEPLAYER_MODE_SELECTION_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
                game = Game(620, 300, 30, 4)
            if multiplayer_button.is_clicked(event):
                GAME_STATE = MULTIPLAYER_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
                if check_internet_connection("www.google.com", 3):
                    multiplayer_error = "Connected to the internet. Connecting to the server..."
                    multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
                    sock = connect_to_server(on_message=show_error)
                    if not sock:
                        multiplayer_error = "Couldnt connect to the server. Please try again later."
                        multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
                    else:
                        multiplayer_error = "Successfully connected to the server."
                        multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
                else:
                    multiplayer_error = "Your device is offline. Please connect to the internet."
                    multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))

            if options_button.is_clicked(event):
                color_scheme_grid = game.initialize_color_scheme_squares(all_colors)
                GAME_STATE = OPTIONS_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
            if tutorial_button.is_clicked(event):
                GAME_STATE = TUTORIAL_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")

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
                                sound_manager.play_sound("block")
                                if score > high_score:
                                    high_score_value = ui_font.render(str(score), 1, (255, 255, 255))
                                game_over_message = game.is_game_over()
                                if game_over_message == "You won":
                                    sound_manager.stop_music()
                                    sound_manager.play_sound("cheer")
                                    # No need to write new row in a database if I can just update the existing one
                                    if not won_any_game:
                                        set_score(score, CURRENT_GAME_MODE)
                                    else:
                                        update_score(score, CURRENT_GAME_MODE)
                                    won_any_game = True
                                elif game_over_message == "No moves left":
                                    sound_manager.stop_music()
                                    sound_manager.play_sound("laugh")
                                    if won_any_game:
                                        update_score(score, CURRENT_GAME_MODE)
                                if won_any_game:
                                    update_score(score, CURRENT_GAME_MODE)
            # TODO every back button needs to fix the game state
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
                game = Game(620, 300, 30, 4)
                default_scheme = get_colorscheme()
                CURRENT_GAME_MODE = ""
                game_over_message = ""
                score = 0
                score_value = ui_font.render(str(score), 1, (255, 255, 255))
                won_any_game = False
                sound_manager.play_sound("click")
                if not pygame.mixer.music.get_busy():
                    sound_manager.play_music()
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
            if game_over_message == "You won" and new_game_button.is_clicked(event):
                game_over_message = ""
                game = Game(620, 300, 30, 4)
                default_scheme = get_colorscheme()

                if CURRENT_GAME_MODE == "Standard":
                    game.colors = all_colors[default_scheme][:4]
                else:
                    game.colors = all_colors[default_scheme]
                game.initialize_grid()
                sound_manager.play_sound("click")
                sound_manager.play_music()
            elif game_over_message == "No moves left" and new_game_button.is_clicked(event):
                game_over_message = ""
                game = Game(620, 300, 30, 4)
                default_scheme = get_colorscheme()

                if CURRENT_GAME_MODE == "Standard":
                    game.colors = all_colors[default_scheme][:4]
                else:
                    game.colors = all_colors[default_scheme]
                game.initialize_grid()
                score = 0
                score_value = ui_font.render(str(score), 1, (255, 255, 255))
                won_any_game = False
                sound_manager.play_sound("click")
                sound_manager.play_music()
        elif GAME_STATE == SINGLEPLAYER_MODE_SELECTION_STATE:
            if standard_singleplayer_mode_button.is_clicked(event):
                game.colors = all_colors[default_scheme][:4]
                game.initialize_grid()
                GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                PREVIOUS_GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                CURRENT_GAME_MODE = "Standard"
                high_score = get_max_score(CURRENT_GAME_MODE)
                high_score_value = ui_font.render(str(high_score), 1, (255, 255, 255))
                sound_manager.play_sound("click")
            if color_madness_singleplayer_mode_button.is_clicked(event):
                game.colors = all_colors[default_scheme]
                game.initialize_grid()
                GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                PREVIOUS_GAME_STATE = SINGLEPLAYER_SCREEN_STATE
                CURRENT_GAME_MODE = "ColorMadness"
                high_score = get_max_score(CURRENT_GAME_MODE)
                high_score_value = ui_font.render(str(high_score), 1, (255, 255, 255))
                sound_manager.play_sound("click")
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
        elif GAME_STATE == MULTIPLAYER_SCREEN_STATE:
            if not is_in_match and join_lobby_button.is_clicked(event):
                validation_result = is_valid_nickname(multiplayer_nickname)
                if validation_result is True:
                    if sock:
                        send_message(sock, "CHECK_NICKNAME", {"nickname": multiplayer_nickname})
                        is_nickname_set = True
                    else:
                        multiplayer_error = "Can't connect to the server. Please try again later."
                        multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
                else:
                    multiplayer_error = validation_result
                    multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
            # TODO match can be found even without nickname - need to update the if condition
            if not is_in_match and find_match_button.is_clicked(event):
                send_message(sock, "MATCHMAKING", {"nickname": multiplayer_nickname})
                multiplayer_error = "Finding a match."
                multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
                mp_game = Game(238, 300, 30, 4)
                mp_game.colors = all_colors[default_scheme][:4]
                mp_game.initialize_grid()
                is_in_match = True
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
                multiplayer_error = "Connecting to the server..."
                multiplayer_error_text = small_ui_font.render(multiplayer_error, 1, (255, 255, 255))
            # if opponents_name is not None:
            #     send_message(sock, "GRID", {"nickname": opponents_name, "grid": mp_game.grid})
            if opponents_name is not None:
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, row in enumerate(mp_game.grid):
                        for j, cell in enumerate(row):
                            if cell is not None:
                                rect, color = cell
                                if rect.collidepoint(pos):
                                    connected_squares_len = mp_game.handle_move(i, j, color)
                                    score += add_score(connected_squares_len)
                                    score_value = ui_font.render(str(score), 1, (255, 255, 255))
                                    send_message(sock, "MOVE",{"nickname": multiplayer_nickname, "square_description": [i, j, color]})

        elif GAME_STATE == OPTIONS_SCREEN_STATE:
            if music_up_button.is_clicked(event):
                if music_level_value < 10:
                    music_level_value += 1
                    sound_manager.set_music_volume(music_level_value)
                    music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
                    set_musiclevel(music_level_value)
                sound_manager.play_sound("click")
            if music_down_button.is_clicked(event):
                if music_level_value > 0:
                    music_level_value -= 1
                    sound_manager.set_music_volume(music_level_value)
                    music_level_value_text = ui_font.render(str(music_level_value), 1, (255, 255, 255))
                    set_musiclevel(music_level_value)
                sound_manager.play_sound("click")
            if sound_up_button.is_clicked(event):
                if sound_level_value < 10:
                    sound_level_value += 1
                    sound_manager.set_sound_volume(sound_level_value)
                    sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
                    set_soundlevel(sound_level_value)
                sound_manager.play_sound("click")
            if sound_down_button.is_clicked(event):
                if sound_level_value > 0:
                    sound_level_value -= 1
                    sound_manager.set_sound_volume(sound_level_value)
                    sound_level_value_text = ui_font.render(str(sound_level_value), 1, (255, 255, 255))
                    set_soundlevel(sound_level_value)
                sound_manager.play_sound("click")
            if color_scheme_1.is_clicked(event):
                if PREVIOUS_GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
                    game.swap_color_palette(all_colors[default_scheme], all_colors[0])
                # TODO If I am in multiplayer does the color palette change when I use the mp_game Game object?
                # TODO also do i want to send this change to my opponent?
                # elif PREVIOUS_GAME_STATE == MULTIPLAYER_SCREEN_STATE:
                #     mp_game.swap_color_palette()
                default_scheme = 0
                set_colorscheme(default_scheme)
                sound_manager.play_sound("click")
            if color_scheme_2.is_clicked(event):
                if PREVIOUS_GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
                    game.swap_color_palette(all_colors[default_scheme], all_colors[1])
                default_scheme = 1
                set_colorscheme(default_scheme)
                sound_manager.play_sound("click")
            if color_scheme_3.is_clicked(event):
                if PREVIOUS_GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
                    game.swap_color_palette(all_colors[default_scheme], all_colors[2])
                default_scheme = 2
                set_colorscheme(default_scheme)
                sound_manager.play_sound("click")
            if color_scheme_4.is_clicked(event):
                if PREVIOUS_GAME_STATE == SINGLEPLAYER_SCREEN_STATE:
                    game.swap_color_palette(all_colors[default_scheme], all_colors[3])
                default_scheme = 3
                set_colorscheme(default_scheme)
                sound_manager.play_sound("click")
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")
        elif GAME_STATE == TUTORIAL_SCREEN_STATE:
            if back_button.is_clicked(event):
                GAME_STATE = TITLE_SCREEN_STATE
                PREVIOUS_GAME_STATE = TITLE_SCREEN_STATE
                sound_manager.play_sound("click")

    # No need of pygame events
    if GAME_STATE == TITLE_SCREEN_STATE:
        animate_title(title, FULL_HD_RESOLUTION, elapsed_time)
        screen.blit(title['surface'], title['rect'])
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
        if game_over_message == "You won":
            screen.blit(win_text, win_text_rect)
            new_game_button.draw(screen)
        elif game_over_message == "No moves left":
            screen.blit(lose_text, lose_text_rect)
            new_game_button.draw(screen)
    elif GAME_STATE == SINGLEPLAYER_MODE_SELECTION_STATE:
        standard_singleplayer_mode_button.draw(screen)
        color_madness_singleplayer_mode_button.draw(screen)
        back_button.draw(screen)
    # TODO bug - during a game buttons are hidden but still clickable(check nick, find a game)
    elif GAME_STATE == MULTIPLAYER_SCREEN_STATE:
        if is_nickname_set:
            multiplayer_nickname_surface = ui_font.render(multiplayer_nickname, True, (255, 255, 255))
            multiplayer_nickname_rect = multiplayer_nickname_surface.get_rect(center=(FULL_HD_RESOLUTION[0] // 4, 140))
            screen.blit(multiplayer_nickname_surface, multiplayer_nickname_rect)
            if opponents_name is not None:
                opponents_name_text = ui_font.render(opponents_name, True, (255, 255, 255))
                # TODO This is not centered to the other half of the screen
                opponents_name_rect = opponents_name_text.get_rect(
                    center=(FULL_HD_RESOLUTION[0] * 3 // 4, 140))
                multiplayer_nickname_rect = multiplayer_nickname_surface.get_rect(
                    center=(FULL_HD_RESOLUTION[0] // 4, 140))
                screen.blit(opponents_name_text, opponents_name_rect)
                screen.blit(multiplayer_nickname_surface, multiplayer_nickname_rect)
                pygame.draw.line(screen, 'black', (FULL_HD_RESOLUTION[0] // 2, 0),
                                 (FULL_HD_RESOLUTION[0] // 2, 790), width=2)

                screen.blit(score_text, (210, 870))
                screen.blit(score_value, (360, 870))
                screen.blit(enemy_score_text, (1150, 870))
                screen.blit(enemy_score_value, (1570, 870))


                pos = pygame.mouse.get_pos()
                for i, row in enumerate(mp_game.grid):
                    for j, cell in enumerate(row):
                        if cell is not None:
                            rect, color = cell
                            if rect.collidepoint(pos):
                                connected_squares = mp_game.find_connected_squares(i, j, color)
                                if len(connected_squares) > 1:
                                    mp_game.highlight_connected_squares(connected_squares, screen)
                mp_game.draw(screen)
                if len(opponents_board.grid) > 0:
                    opponents_board.draw(screen)
            # TODO this condition is not the best - this should be displayed only when they dont play
            if not is_in_match:
                find_match_button.draw(screen)
        else:
            screen.blit(enter_nickname_text, enter_nickname_text_rect)
            if active_nickname_text_box:
                nickname_text_box_color = pygame.Color((0, 0, 0))
            else:
                nickname_text_box_color = pygame.Color((255, 255, 255))
            pygame.draw.rect(screen, nickname_text_box_color, multiplayer_nickname_text_box, 1)
            multiplayer_nickname_surface = ui_font.render(multiplayer_nickname, True, (255, 255, 255))
            screen.blit(multiplayer_nickname_surface, (multiplayer_nickname_text_box.x + 5, multiplayer_nickname_text_box.y))
            multiplayer_nickname_text_box.w = max(100, multiplayer_nickname_surface.get_width() + 10)
            if not is_in_match:
                join_lobby_button.draw(screen)
        screen.blit(multiplayer_error_text, multiplayer_error_text_rect)
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
            pygame.draw.line(screen, (0, 0, 0), (680, 660), (870, 660), 5)
        elif default_scheme == 1:
            pygame.draw.line(screen, (0, 0, 0), (1060, 660), (1250, 660), 5)
        elif default_scheme == 2:
            pygame.draw.line(screen, (0, 0, 0), (680, 790), (870, 790), 5)
        elif default_scheme == 3:
            pygame.draw.line(screen, (0, 0, 0), (1060, 790), (1250, 790), 5)
    elif GAME_STATE == TUTORIAL_SCREEN_STATE:
        screen.blit(tutorial_text_1, tutorial_text_1_rect)
        screen.blit(tutorial_text_2, tutorial_text_2_rect)
        screen.blit(tutorial_text_3, tutorial_text_3_rect)
        screen.blit(tutorial_text_4, tutorial_text_4_rect)
        screen.blit(tutorial_text_5, tutorial_text_5_rect)
        screen.blit(tutorial_text_6, tutorial_text_6_rect)
        back_button.draw(screen)

    quit_button.draw(screen)
    pygame.display.flip()

pygame.quit()
