import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            # "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            # "match": pygame.mixer.Sound("assets/sounds/match.wav"),
            # "fall": pygame.mixer.Sound("assets/sounds/fall.wav"),
        }
        self.music_file = "../assets/sounds/Neo soul loopsy.wav"
        self.music_toggle = True

    def play_music(self):
        if self.music_toggle:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)  # -1 = opakovane
