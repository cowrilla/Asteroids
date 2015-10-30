import pygame, sys, classes, random



# all the event happen in this function
def process(ship, fps, total_frames, screen_size, start_sprite, exit_sprite):
			
	score = 0 # start a score counter
	


	controls(ship, fps, total_frames, screen_size, start_sprite, exit_sprite)

	got_gift = gift_pack_spawn(fps, total_frames, screen_size)
	score += off_screen(screen_size)
	score += asteriod_collision(ship, classes.FighterShip.sprite_list) 	
	gift_collision(ship)
	background(fps, total_frames, screen_size)
	asteroid_spawn(fps, total_frames, screen_size)

	if ship.health == 0: # dead

		try:
			for i in classes.Asteroids.sprite_list: # removes star and astroid sprites from list after they left screenS

				i.destroy(classes.Asteroids)
				i.destroy(classes.GiftPack)
 
			print('DEAD!')
		except:
			pass

		return True, score # if dead 

	return False, score # while alive


# all input from user
def controls(ship, fps, total_frames, screen_size, start_sprite, exit_sprite):

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		keys = pygame.key.get_pressed()

		if event.type == pygame.KEYUP:
			ship.velx = 0
			ship.vely = 0
			ship.image = pygame.image.load('images/ship/plane.png')
		
		if keys[pygame.K_w]:
			ship.vely = -8
			ship.image = pygame.image.load('images/ship/plane_speed.png')

		if keys[pygame.K_s]:
			ship.vely = 4 
			ship.image = pygame.image.load('images/ship/plane_slow.png')

		if keys[pygame.K_d]:
			ship.velx = 7
			ship.image = pygame.image.load('images/ship/plane_right.png')

		if keys[pygame.K_a]:
			ship.velx = -7
			ship.image = pygame.image.load('images/ship/plane_left.png')

		
		# start game 
		if pygame.sprite.spritecollide(start_sprite, classes.FighterShip.sprite_list, False):

			if keys[pygame.K_RETURN]:
				ship.health = 35
				
				return False
		# exit game
		if pygame.sprite.spritecollide(exit_sprite, classes.FighterShip.sprite_list, False):

			if keys[pygame.K_RETURN]:
				pygame.quit()
				sys.exit()


	# seperate for fire command 
	keys = pygame.key.get_pressed()

	if ship.ammo > 0: 
		if keys[pygame.K_SPACE]:
			classes.Projectile(ship.rect.x + 10, ship.rect.y - 6 , -11, ship, 'images/ship/shot.png', fps, total_frames, screen_size)



	return True # while enter is not pressed


# 
def background(fps, total_frames, screen_size):

	ran_spawn = (random.randint(1, 3) * .05) # set random spawn count
	spawn_time = fps * ran_spawn # convet it to seconds
	star_list = ('images/stars/star.png', 'images/stars/star1.png', 'images/stars/star2.png', 'images/stars/star3.png', 'images/stars/star4.png') # list of stars
	rand_star_int = random.randint(0, len(star_list)-1) # pick a star out of list
	if total_frames % spawn_time == 0: # 
		x = random.randint(0, screen_size[0]) # randomize the x location

		classes.Background(x, -60, star_list[rand_star_int]) # 


# 
def asteroid_spawn(fps, total_frames, screen_size):

	interval = .2 # spawn timer
	spawn_time = fps * interval

	if total_frames % spawn_time == 0:
		hp = random.randint(1, 5) # spawn health

		x = random.randint(4, screen_size[0] - 44) # spawn location
		# spawn image
		if hp == 1:
			classes.Asteroids(x, -60, hp, 'images/asteroid/asteroid3.png')
		elif hp > 1 and hp < 4:
			classes.Asteroids(x, -60, hp, 'images/asteroid/asteroid2.png')
		else:
			classes.Asteroids(x, -60, hp, 'images/asteroid/asteroid.png')


# 
def gift_pack_spawn(fps, total_frames, screen_size):
	interval = 20
	spawn_time = fps * interval

	if total_frames % spawn_time == 0:
		x = random.randint(4, screen_size[0] - 44)
		classes.GiftPack(x, -60, 'images/misc/bonus.png')
		#return  True

		#return False


# delets sprites from list after they are off the screen
def off_screen(screen_size): 
	score = 0 

	# use try so when list is empty there is no error
	try:
		for i in classes.Projectile.normal_list: # removes projectiles from list after they leave screen
			if i.rect.y < -200: # 
				i.destroy()
	except:
		pass

	try:
		for i in classes.Asteroids.sprite_list: # removes star and astroid sprites from list after they left screenS

			if i.rect.y > screen_size[1] + 200:
				i.destroy(classes.Asteroids)
				score += 0.4 

		for i in classes.Background.sprite_list:

			if i.rect.y > screen_size[1] + 200:
				i.destroy(classes.Background)  
				score += 0.4  
	except:
		pass

	return score


# asteriod collition with projectile and ship
def asteriod_collision(ship, ClassName):  
	score = 0

	for asteriod in classes.Asteroids.sprite_list:

		# if ship hit
		if pygame.sprite.spritecollide(asteriod, ClassName, False): 
		

			ship.health -= 1
			score += 1
			asteriod.health -= 1

			if asteriod.health > 1 and asteriod.health < 4:
				asteriod.image = pygame.image.load('images/asteroid/asteroid2.png')
				score += 1
			elif asteriod.health == 1:
				asteriod.image = pygame.image.load('images/asteroid/asteroid3.png')	
				score += 1			
			elif asteriod.health <= 0:
				asteriod.destroy(classes.Asteroids)
				score += 10
			else:
				pass

			if ship.health <= 0:
	
				ship.health = 0

		# if projectile hit
		if pygame.sprite.spritecollide(asteriod, classes.Projectile.sprite_list, True):
			score += 1
			asteriod.health -= 1
			if asteriod.health > 1 and asteriod.health < 4:
				asteriod.image = pygame.image.load('images/asteroid/asteroid2.png')
				score += 1
			elif asteriod.health == 1:
				asteriod.image = pygame.image.load('images/asteroid/asteroid3.png')	
				score += 1			
			elif asteriod.health <= 0:
				asteriod.destroy(classes.Asteroids)
				score += 10
			else:
				pass
			

	return score


# simple gift collisin with ship or projectile
def gift_collision(ship): 

	for gift in classes.GiftPack.sprite_list:
		if pygame.sprite.spritecollide(gift, classes.FighterShip.sprite_list, False) \
		 or pygame.sprite.spritecollide(gift, classes.Projectile.sprite_list, True):
			gift_chance = random.randint(1, 20)
			if gift_chance <= 14:

				ship.ammo += 15
				if ship.ammo >= 1000:
					ship.ammo = 1000

			else:
				ship.health += 5
				if ship.health >= 100:
					ship.health = 100
				

			gift.destroy(classes.GiftPack)




