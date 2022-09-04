# Author: John Brown
# Artist: Amber Vue Brown
# GitHub username: brown-science
# Date: 6/20/2022
# Description: Modified game from "The ultimate introduction to Pygame"
# YouTube tutorial published by the Clear Code channel

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Art/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Art/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Art/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
        #self.jump_sound.set_volume( )

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load('Art/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Art/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Art/snail/Fetti1(1).png').convert_alpha()
            snail_1 = pygame.transform.rotozoom(snail_1, 0, 2)
            snail_2 = pygame.image.load('Art/snail/Final Fetti (2).png').convert_alpha()
            snail_2 = pygame.transform.rotozoom(snail_2, 0, 2)
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

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
            self.kill

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render('Score:  ' f'{current_time}', False, 'Blue')
    score_rect = score_surf.get_rect(center = (400, 60))
    screen.blit(score_surf, score_rect)
    return current_time

# def obstacle_movement(obstacle_list):
#     if obstacle_list: #If list is not empty, empty list = False in python
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 6
#
#             if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
#             else: screen.blit(fly_surf, obstacle_rect)
#
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#
#         return obstacle_list
#     else: return []

# #def collisions(player, obstacles):
#     if obstacles:
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect): return False
#     return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): #returns empty list if no collision
        obstacle_group.empty()
        return  False
    else: return True

def player_animation():
    global player_surf, player_index
    """Play walking animation if player on floor"""
    # Play jump if player not on floor
    if player_rect.bottom < 300: #jump
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index )]

pygame.init() # ESSENTIAL initiates how to display images, play sound, etc
screen = pygame.display.set_mode((800, 400))  # width, height of game window
pygame.display.set_caption("Jumpin' Fettys")
clock = pygame.time.Clock() # creates a clock object of the class Clock
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)  # font type, font size
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

back_surf = pygame.image.load('Art/background.png').convert_alpha()  # converts to form python reads better
#ground_surf = pygame.image.load('./Art/ground.png').convert_alpha()

# score_surf = test_font.render("Jumpin' Fettys", False, 'Blue')  # text, anti alias(smooth text edges), color
# score_rect = score_surf.get_rect(center = (400, 60))

# Snail
snail_frame_1 = pygame.image.load('Art/snail/Fetti1(1).png').convert_alpha()
snail_frame_2 = pygame.image.load('Art/snail/Fetti 2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('Art/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Art/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []


player_walk_1 = pygame.image.load('Art/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Art/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Art/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Art/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # surface, angle, scale
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = test_font.render("Jumpin' Fettys", False, 'Blue')  # text, anti alias(smooth text edges), color
title_rect = title_surf.get_rect(center = (400, 60))

instruction_surf = test_font.render("Press space to jump", False, 'Blue')
instruction_rect = instruction_surf.get_rect(center = (400, 340))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    # draw all elements, update everything
    # everything under while loop will be displayed to user
    for event in pygame.event.get(): # pygame.event.get() gets all possible user inputs. This is an event loop, with every frame, it checks player input and then uses the code below to generate an image.
        if event.type == pygame.QUIT: # pygame.QUIT is synonomus to X button
            pygame.quit()
            exit() # sys module that closes code
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: player_gravity = -20

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
            #         player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0,2): # gives 0 or 1, randomly gives T or F
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                # else: obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 200)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
            else: fly_frame_index = 0
            fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)



    if game_active:
        screen.blit(back_surf, (0, 0)) # surface, (x,y) # blit means block image transfer # puts one surface on another
        #screen.blit(ground_surf, (0, 300))
        score = display_score()
        bg_music = pygame.mixer.Sound('./audio/music.wav')
        bg_music.set_volume(0.1)
        bg_music.play(loops = -1) #loops forever

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        # Obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collision_sprite()
        #game_active = collisions(player_rect, obstacle_rect_list)


    else:
        screen.fill((94,129,162)) #rgb color
        screen.blit(snail_frame_1, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (600, 300) # in case you die during jump
        player_gravity = 0 # in case you die suring jump

        score_message = test_font.render(f'Your score:  {score}', False, 'Blue')
        score_message_rect = score_message.get_rect(center = (400, 340))
        screen.blit(title_surf, title_rect)

        if score == 0: screen.blit(instruction_surf, instruction_rect)
        else: screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)  # While true, run while loop 60 times per second