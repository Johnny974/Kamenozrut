import pygame

# TODO Need to add sounds and new music
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            # "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            # "match": pygame.mixer.Sound("assets/sounds/match.wav"),
            # "fall": pygame.mixer.Sound("assets/sounds/fall.wav"),
        }
        self.music_file = "../assets/sounds/Neo soul loopsy.wav"

    def play_music(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)  # -1 = opakovane

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 10)

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume / 10)