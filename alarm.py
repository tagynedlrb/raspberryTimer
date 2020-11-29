import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'
import pygame
import time

pygame.mixer.init()
#alarm1 = pygame.mixer.music.load("alarm1.mp3")
alarm1 = pygame.mixer.Sound("alarm1.mp3")

while True:
	alarm1.play()
#	pygame.mixer.music.start()
	time.sleep(2)
