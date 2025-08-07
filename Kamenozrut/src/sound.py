import pygame
import random


# TODO Need to add sounds and new music
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "block": pygame.mixer.Sound("../assets/sounds/block_hit.ogg"),
            "click": pygame.mixer.Sound("../assets/sounds/tic-toc-click.wav"),
            "laugh": pygame.mixer.Sound("../assets/sounds/witchy-laugh.wav"),
            "cheer": pygame.mixer.Sound("../assets/sounds/crowd-cheer.wav")
        }
        self.music_files = ["../assets/sounds/Neo soul loopsy.wav",
                            "../assets/sounds/Pixel Nostalgia.wav"]
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        self.MUSIC_DELAY_EVENT = pygame.USEREVENT + 2
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def play_music(self):
        pygame.mixer.music.load(random.choice(self.music_files))
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 10)

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume / 10)

    def play_sound(self, sound):
        self.sounds[sound].play()
