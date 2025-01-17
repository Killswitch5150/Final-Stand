import pygame
import time  #for delay

#--customization--
# these are the only variables needed to change splash screen display properties

splash_screen_path = "./splash/img/frontlinestudios_logo_1080.png"
#provide string literal to image you want to be displayed on the splash screen
#default is: "./splash/img/frontlinestudios_logo_1080.png"

splash_screen_scale_factor = 0.4
#provide float value for scale of the original image file to fit the splash screen
#default is: 0.4

splash_screen_timer_duration = 3000
#provide integer value for duration of how long the splash screen should be shown
#default is: 3000 (3 seconds)

splash_img_pos = (25, 80)
#provide tuple value for position of image to be displayed
#default is (25, 80)

#--

def load_and_scale_image(path, scale_factor):  
    image = pygame.image.load(path).convert_alpha() 
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))  # Return scaled image

def run_splash_screen(image_path=splash_screen_path, scale_factor=splash_screen_scale_factor, timer_duration=splash_screen_timer_duration):
    pygame.init()

    game_resolution = (800, 600)
    window = pygame.display.set_mode(game_resolution, pygame.DOUBLEBUF, 24)
    image = load_and_scale_image(image_path, scale_factor)

    start_ticks = pygame.time.get_ticks() #start timer

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  #quit if the window is closed, allows player to skip splash screens

        elapsed_time = pygame.time.get_ticks() - start_ticks

        if elapsed_time >= timer_duration:
            print("Timer finished. Next scene loading.")

            time.sleep(1) 
            
            running = False  #when timer is finished end loop

        
        window.fill((0, 0, 0))  #black background
        window.blit(image, splash_img_pos)  #draw image
        
        pygame.display.update()
