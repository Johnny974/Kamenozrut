import pygame
import random

# TODO Need to add sounds and new music
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            # "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            # "match": pygame.mixer.Sound("assets/sounds/match.wav"),
            # "fall": pygame.mixer.Sound("assets/sounds/fall.wav"),
        }
        self.music_files = ["../assets/sounds/Neo soul loopsy.wav",
                           "../assets/sounds/Pixel Nostalgia.wav"]
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        self.MUSIC_DELAY_EVENT = pygame.USEREVENT + 2
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def play_music(self):
        pygame.mixer.music.load(random.choice(self.music_files))
        pygame.mixer.music.play()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 10)

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume / 10)