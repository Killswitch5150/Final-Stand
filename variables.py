import pygame 

varGameName = "Final Stand" #name of the game to appear on window and UI
screen_size_choice_fullscreen = False #default value for fullscreen toggle
width, height = 800, 600  # window size vars
game_resolution = (width, height) #put window size tuple into game_resolution var
bullet_ready_to_shoot = True #starts playing with shooting action enabled
bullets, enemies, ammo_boxes = [], [], [] #declares empty lists to be written during gameplay

#sound initialization vars
s_freq = 44100
s_size = 16
s_channel = 2 
s_buffer = 4096

#initiating pygame, setting up window settings and vars
pygame.mixer.pre_init(s_freq, s_size, s_channel, s_buffer) #initializing audio support
pygame.init() #initiating pygame 
pygame.display.set_caption(varGameName) #set window text to name of the game
window = pygame.display.set_mode((game_resolution), pygame.DOUBLEBUF, 24)  # window size set to game res
