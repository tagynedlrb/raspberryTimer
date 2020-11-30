import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'
import pygame
import time

pygame.mixer.init()

def alart_1min_left():
	alart_1min = pygame.mixer.Sound("./sounds/alart_1min.mp3")
	alart_1min.play()
	time.sleep(3)
	pygame.mixer.pause()

def rooster():
	rooster = pygame.mixer.Sound("./sounds/rooster.mp3")
	rooster.play()
