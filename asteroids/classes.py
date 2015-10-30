import pygame, random, math



# base class that other objects will inherate from
class BaseClass(pygame.sprite.Sprite): # inherates contains collision detection, motion, drawing
	
	
	def __init__(self, x, y, image_str):
		pygame.sprite.Sprite.__init__(self) # calls the sprite classes gives us access to variables

		self.image = pygame.image.load(image_str) # actual image (image gives h & w)
		self.rect = self.image.get_rect() # the actual square of the image x, y, w, h, 
		self.rect.x = x # initial start
		self.rect.y = y # initial start



	def destroy(self, ClassName): # remove sprites
		ClassName.sprite_list.remove(self)
		del self



class FighterShip(BaseClass): # the ship and movements restrictions

	sprite_list = pygame.sprite.Group() # list of all ship sprites
	def __init__(self, x, y, health, ammo, image_str): # will be calling all the base classes constructors
		BaseClass.__init__(self,  x, y, image_str) # calls all of BaseClass
		FighterShip.sprite_list.add(self) # update list
		self.velx, self.vely = 0, 0 # movement speed
		self.health = health
		self.ammo = ammo

	def motion(self, screen_size): # movement

		predict_loc_x = self.rect.x + self.velx # looks to see if next move will be off screen
		predict_loc_y = self.rect.y + self.vely 


		# stay on screen
		if predict_loc_x < 0: 
			self.velx = 0
		elif predict_loc_x + self.rect.width > screen_size[0]:
			self.velx = 0

		# small y restrictions
		if predict_loc_y < (screen_size[1] * 0.04):
			self.vely = 0
		elif predict_loc_y + self.rect.height > (screen_size[1] * 0.92):
			self.vely = 0


		self.rect.x += self.velx
		self.rect.y += self.vely



class Background(BaseClass): # simple add stars to screen with motion

	sprite_list = pygame.sprite.Group()

	def __init__(self, x, y, image_str):
		BaseClass.__init__(self, x, y, image_str)
		Background.sprite_list.add(self)
		self.vely = random.randint(1, 25)


	def moving_star(self, screen_size):
		self.rect.y += self.vely

	@staticmethod
	def get_moving(screen_size):

		for star in Background.sprite_list:
			
			star.moving_star(screen_size)



class Asteroids(BaseClass): # creat asteroids 

	sprite_list = pygame.sprite.Group() # list to keep track of all 

	def __init__(self, x, y, health, image_str):
		BaseClass.__init__(self, x, y, image_str)
		Asteroids.sprite_list.add(self) # update list when new one is made

		self.vely = random.randint(1, 4)
		self.health = health

	def enemy_moving(self, screen_size):
		self.rect.y += self.vely



	@staticmethod
	def moving_enemy(fps, total_frames, screen_size):

		for enemy in Asteroids.sprite_list:

			enemy.enemy_moving(screen_size)
			#enemy.enemy_fire(fps, total_frames, screen_size)



class GiftPack(BaseClass): # # gift pack for hp or ammo replenishment

	sprite_list = pygame.sprite.Group()
	def __init__(self, x, y, image_str):
		BaseClass.__init__(self, x, y, image_str)
		GiftPack.sprite_list.add(self)
		self.vely = 2

	def movement(self, screen_size):
		self.rect.y += self.vely

	@staticmethod
	def moving_gift(fps, total_frames, screen_size):

		for gift in GiftPack.sprite_list:

			gift.movement(screen_size)



class StartMenu(BaseClass): # simple start menu control

	sprite_list = pygame.sprite.Group()
	def __init__(self, x, y, image_str):
		BaseClass.__init__(self, x, y, image_str)
		StartMenu.sprite_list.add(self)



class Projectile(pygame.sprite.Sprite): # porjectiles
	location = 0
	sprite_list = pygame.sprite.Group() # list of sprites
	normal_list = [] # basic list for sprite control
	def __init__(self, x, y, vely, ship, image_str, fps, total_frames, screen_size):
		
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_str)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.shit = ship
		self.vely = vely
		self.fps = fps
		self.total_frames = total_frames
		self.screen_size = screen_size

		# make sure cant fire more then evey 0.2 seconds
		interval = .2 
		spawn_time = fps * interval

		# keep track of ammo count
		if total_frames % spawn_time != 0:
			return
		else:
			if ship.ammo > 0:
				ship.ammo -=1
			else:
				ship.ammo = 0

		Projectile.sprite_list.add(self) # add to sprite list
		Projectile.normal_list.append(self) # add to normal list

	@staticmethod # call our fire method
	def fired():

		for projectile in Projectile.sprite_list:
			projectile.rect.y += projectile.vely


	def destroy(self): # remove the sprite

		Projectile.sprite_list.remove(self)
		Projectile.normal_list.remove(self)
		del self



class TextToScreen(object): # simple text to screen

	def __init__(self, x, y, size, color):
		self.x = x
		self.y = y
		self.size = size
		self.color = color


	def text_return(self, screen, text):

		self.init_font = pygame.font.SysFont('MS serif', self.size)
		self.rendered = self.init_font.render(text, True, self.color)
		screen.blit(self.rendered, (self.x, self.y))





