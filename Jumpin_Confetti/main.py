import asyncio
import pygame
import math
from sys import exit
import random
from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF

# Make global variables
# Move pygame init files to top
# Ensure image varibles are loaded properly

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#player_walk_1 = pygame.image.load('./assets/Player/walk-1-md.png')
		#player_walk_2 = pygame.image.load('./assets/Player/walk-2-md.png')
		self.player_walk = [player_walk_1, player_walk_2]
		self.player_index = 0
		self.player_jump = player_jump

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom=(80, 420))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 420:
			self.gravity = -20
			#self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 420:
			self.rect.bottom = 420

	def animation_state(self):
		if self.rect.bottom < 420:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

# Loading assets
pygame.init()
screen = pygame.display.set_mode((1200,471))
dog_frame_1 = pygame.image.load('./assets/Dog/Confetti-1-sm.png').convert_alpha()
dog_frame_2 = pygame.image.load('./assets/Dog/Confetti-2-sm.png').convert_alpha()
dog_frame_3 = pygame.image.load('./assets/Dog/Confetti-3-sm.png').convert_alpha()
dog_1 = pygame.image.load('./assets/Dog/Confetti-1-sm.png').convert_alpha()
dog_2 = pygame.image.load('./assets/Dog/Confetti-2-sm.png').convert_alpha()
dog_3 = pygame.image.load('./assets/Dog/Confetti-3-sm.png').convert_alpha()
back_trees_surface = pygame.image.load('./assets/Background/forest-back-trees.png').convert_alpha()
sky_surface = pygame.image.load('./assets/Background/forest-lights.png').convert_alpha()
mid_trees_surface = pygame.image.load('./assets/Background/forest-middle-trees.png').convert_alpha()
front_trees_surface = pygame.image.load('./assets/Background/forest-front-trees.png').convert_alpha()
player_walk_1 = pygame.image.load('./assets/Player/walk-1-md.png').convert_alpha()
player_walk_2 = pygame.image.load('./assets/Player/walk-2-md.png').convert_alpha()
player_jump = pygame.image.load('./assets/Player/jump-md2.png').convert_alpha()


async def main():

	class Obstacle(pygame.sprite.Sprite):
		def __init__(self,type):
			super().__init__()

			self.frames = [dog_1, dog_2, dog_3]
			y_pos  = 420

			self.animation_index = 0
			self.image = self.frames[self.animation_index]
			self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

		def animation_state(self):
			self.animation_index += 0.1
			if self.animation_index >= len(self.frames): self.animation_index = 0
			self.image = self.frames[int(self.animation_index)]

		def update(self):
			self.animation_state()
			self.rect.x -= 8
			self.destroy()

		def destroy(self):
			if self.rect.x <= -100:
				self.kill()


	def display_score():
		current_time = int(pygame.time.get_ticks() / 1000) - start_time
		score_surf = test_font.render(f'Score: {current_time}',False,(64, 83, 102))
		score_rect = score_surf.get_rect(center = (600,50))
		screen.blit(score_surf,score_rect)
		return current_time

	def obstacle_movement(obstacle_list):
		if obstacle_list:
			for obstacle_rect in obstacle_list:
				obstacle_rect.x -= 5

				if obstacle_rect.bottom == 420: screen.blit(dog_surf,obstacle_rect)
				else: screen.blit(obstacle_rect)

			obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

			return obstacle_list
		else: return []

	def collisions(player,obstacles):
		if obstacles:
			for obstacle_rect in obstacles:
				if player.colliderect(obstacle_rect): return False
		return True

	def collision_sprite():
		if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
			obstacle_group.empty()
			return False
		else: return True

	def player_animation():
		global player_surf, player_index

		if player_rect.bottom < 420:
			player_surf = player_jump
		else:
			player_index += 0.1
			if player_index >= len(player_walk):player_index = 0
			player_surf = player_walk[int(player_index)]


	pygame.display.set_caption("Jumpin' Confetti")
	clock = pygame.time.Clock()
	test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
	game_active = False
	start_time = 0
	score = 0
	#bg_music = pygame.mixer.Sound('./audio/music.wav')
	#bg_music.play(loops = -1)

# Required code for web interface

	# Groups
	player = pygame.sprite.GroupSingle()
	player.add(Player())

	obstacle_group = pygame.sprite.Group()



	back_width = back_trees_surface.get_width()
	tiles = math.ceil(1200 / back_width) + 1
	scroll = 0


	# dog

	dog_frames = [dog_frame_1, dog_frame_2, dog_frame_3]
	dog_frame_index = 0
	dog_surf = dog_frames[dog_frame_index]

	obstacle_rect_list = []



	player_walk = [player_walk_1, player_walk_2]
	player_index = 0

	player_surf = player_walk[player_index]
	player_rect = player_surf.get_rect(midbottom = (80,420))
	player_gravity = 0

	# Intro screen
	Confetti = pygame.image.load('./assets/Dog/Confetti_1_md.png')
	Confetti = pygame.transform.rotozoom(Confetti,0,2)
	Confetti_rect = Confetti.get_rect(center = (600,235))

	game_name = test_font.render("Jumpin' Confetti",False,(111,196,169))
	game_name_rect = game_name.get_rect(center = (600,40))

	game_message = test_font.render('Press space to run',False,(111,196,169))
	game_message_rect = game_message.get_rect(center = (600,450))

	# Timer
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer,2500)

	dog_animation_timer = pygame.USEREVENT + 2
	pygame.time.set_timer(dog_animation_timer,500)



	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if game_active:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if player_rect.collidepoint(event.pos) and player_rect.bottom >= 420:
						player_gravity = -20

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and player_rect.bottom >= 420:
						player_gravity = -20
			else:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game_active = True

					start_time = int(pygame.time.get_ticks() / 1000)

			if game_active:
				if event.type == obstacle_timer:
					obstacle_group.add(Obstacle((['dog','dog','dog'])))

				if event.type == dog_animation_timer:
					if dog_frame_index == 0: dog_frame_index = 1
					else: dog_frame_index = 0
					dog_surf = dog_frames[dog_frame_index]


		if game_active:
			for i in range(0, tiles):
				screen.blit(back_trees_surface, (i * back_width + scroll, 0))
				screen.blit(sky_surface, (i * back_width + scroll, 0))
				screen.blit(mid_trees_surface, (i * back_width + scroll, 0))
				screen.blit(front_trees_surface, (i * back_width + scroll, 0))

			score = display_score()
			scroll -= 6
			if abs(scroll) > back_width:
				scroll = 0




			player.draw(screen)
			player.update()

			obstacle_group.draw(screen)
			obstacle_group.update()


			# collision
			game_active = collision_sprite()
		else:
			screen.fill((99, 42, 59))
			screen.blit(Confetti,Confetti_rect)
			obstacle_rect_list.clear()
			player_rect.midbottom = (80,420)
			player_gravity = 0

			score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
			score_message_rect = score_message.get_rect(center = (600,450))
			screen.blit(game_name,game_name_rect)

			if score == 0: screen.blit(game_message,game_message_rect)
			else: screen.blit(score_message,score_message_rect)

		pygame.display.update()
		clock.tick(60)
		await asyncio.sleep(0)  # important for web interface

asyncio.run(main())