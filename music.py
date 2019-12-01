import pygame




class Music(pygame.sprite.Sprite):
    def __init__(self):
        pygame.mixer.init()
        
    def boom(self):
        self.boomSound = pygame.mixer.Sound("music/bang.wav")
        self.boomSound.set_volume(1)
        self.boomSound.play()
    def fire(self):
        self.fireSound = pygame.mixer.Sound("music/Gunfire.wav")
        self.fireSound.set_volume(1)
        self.fireSound.play()
    def start(self):
        self.startSound = pygame.mixer.Sound("music/start.wav")
        self.startSound.set_volume(1)
        self.startSound.play()
