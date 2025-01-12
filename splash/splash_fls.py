import pygame
import time  #for delay

def load_and_scale_image(path, scale_factor):  
    image = pygame.image.load(path).convert_alpha() 
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))  # Return scaled image

def run_splash_screen(image_path="./splash/img/frontlinestudios_logo_1080.png", scale_factor=0.4, timer_duration=3000):
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
        window.blit(image, (25, 80))  #draw image
        
        pygame.display.update()
