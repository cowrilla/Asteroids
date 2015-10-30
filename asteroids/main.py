import pygame, sys
import time, math
from classes import *
from process import process
from start_screen import start

pygame.init()
pygame.font.init()

screen_size = (640, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('*')
clock = pygame.time.Clock()
fps = 60

# number trackers
ammo = 100
total_frames = 0
total_score = 0
hp = 35
max_score = 0
hight_score = 0

# ship sprite
ship = FighterShip((screen_size[0] - 32) * 0.5, screen_size[1] * 0.75, hp, ammo, 'images/ship/plane.png')

# start menu sprites
start_sprite = StartMenu(screen_size[0] * 0.15, screen_size[1] * 0.45, 'images/misc/start.png')
exit_sprite = StartMenu(screen_size[0] * 0.65, screen_size[1] * 0.45, 'images/misc/exit.png')
title_sprite = StartMenu(screen_size[0] * 0.3, screen_size[1] * 0.25, 'images/misc/title.png')
instructions = StartMenu(screen_size[0] * 0.25, screen_size[1] * 0.8, 'images/misc/instructions.png')

# text to screen
score_couter = TextToScreen(screen_size[0] * 0.66, 4, 32, (205, 220, 255))
ammo_track = TextToScreen(screen_size[0] * 0.36, 4, 32, (235, 190, 215))
hp_tracker = TextToScreen(screen_size[0] * 0.01, 4, 32, (180, 255, 190))
game_over = TextToScreen(screen_size[0] * 0.30, screen_size[1] * 0.16, 64, (190, 130, 135))
beta =  TextToScreen(2, screen_size[1] -16, 20, (100, 40, 60))


start_screen = True


# all processes of the game
def game_on(start_screen, ship, total_score, max_score, hight_score, fps, total_frames, screen_size):
	
	# start screen is same as game over screen 
	if start_screen: 

		start_screen = start(ship, fps, total_frames, screen_size, start_sprite, exit_sprite, title_sprite)
		max_score = math.floor(total_score)


		StartMenu.sprite_list.draw(screen)

		if max_score > 0: # game over additions
			score_couter.text_return(screen, 'score: ' + str(max_score))
			game_over.text_return(screen, 'GAME OVER')
		

	if not start_screen: # game screen

		if max_score > 0: # simple test to reset score
			total_score = 0
	

		start_screen, score = process(ship, fps, total_frames, screen_size, start_sprite, exit_sprite) 
		total_score += score
		str_total_score = math.floor(total_score)

		# sprite to screen
		Asteroids.moving_enemy(fps, total_frames, screen_size)
		GiftPack.moving_gift(fps, total_frames, screen_size)

		# text to screen 
		score_couter.text_return(screen, 'score: ' + str(str_total_score))
		ammo_track.text_return(screen, 'ammo: ' + str(ship.ammo))
		hp_tracker.text_return(screen, 'hp: ' + str(ship.health))

	return start_screen, total_score



while True: # main loop

	screen.fill((13, 10, 18))
	clock.tick(fps)


	total_frames += 1 # (total_frames each loop) / fps = 1second

	start_screen, total_score = game_on(start_screen, ship, total_score, max_score, hight_score, fps, total_frames, screen_size)
		
			
	# draw our movements
	ship.motion(screen_size)
	Projectile.fired()
	Background.get_moving(screen_size)

	# draw all our sprites to screen
	Background.sprite_list.draw(screen)
	Asteroids.sprite_list.draw(screen)
	FighterShip.sprite_list.draw(screen)
	Projectile.sprite_list.draw(screen)
	GiftPack.sprite_list.draw(screen)



	beta.text_return(screen, 'cowrilla 2015')
	pygame.display.flip()



pygame.quit()
sys.exit()