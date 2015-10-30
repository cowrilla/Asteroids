import pygame, sys, classes, random
from process import background, off_screen, controls


def start(ship, fps, total_frames, screen_size, start_sprite, exit_sprite, title_sprite):

	ship.ammo = 100

	start_game = controls(ship, fps, total_frames, screen_size, start_sprite, exit_sprite)

	off_screen(screen_size)		
	background(fps, total_frames, screen_size)
	start_animation(ship, start_sprite, exit_sprite, title_sprite)


	return start_game


# start, exit, and title animation contact with ship and projectile
def start_animation(ship, start_sprite, exit_sprite, title_sprite): 
	# title
	if pygame.sprite.spritecollide(title_sprite, classes.Projectile.sprite_list, True): 
	 	title_sprite.image = pygame.image.load("images/misc/title_hit.png")
	else:
	 	title_sprite.image = pygame.image.load("images/misc/title.png")

	# start
	if pygame.sprite.spritecollide(start_sprite, classes.FighterShip.sprite_list, False) \
	 or pygame.sprite.spritecollide(start_sprite, classes.Projectile.sprite_list, True):
		start_sprite.image = pygame.image.load("images/misc/start_high.png")
	else:
		start_sprite.image = pygame.image.load("images/misc/start.png")

	# exit
	if pygame.sprite.spritecollide(exit_sprite, classes.FighterShip.sprite_list, False) \
	 or pygame.sprite.spritecollide(exit_sprite, classes.Projectile.sprite_list, True):
		exit_sprite.image = pygame.image.load("images/misc/exit_high.png")
	else:
		exit_sprite.image = pygame.image.load("images/misc/exit.png")

	



