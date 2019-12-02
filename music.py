import pygame




class Music(pygame.sprite.Sprite):
    def __init__(self):
        pygame.mixer.init()
        self.boomSound = pygame.mixer.Sound("music/bang.wav")
        self.fireSound = pygame.mixer.Sound("music/Gunfire.wav")
        self.startSound = pygame.mixer.Sound("music/start.wav")    
        self.boomSound.set_volume(1)  
        self.fireSound.set_volume(1)
        self.startSound.set_volume(1)
    def boom(self):       
        self.boomSound.play()
    def fire(self):     
        self.fireSound.play()
    def start(self):
        self.startSound.play()
    def closeMusic(self):
        self.boomSound.set_volume(0)
        self.fireSound.set_volume(0)
        self.startSound.set_volume(0)
