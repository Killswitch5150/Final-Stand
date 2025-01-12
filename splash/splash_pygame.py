import pygame
import time  #for delay

#for code reference, better comments, etc. reference 'splash_fls.py' file

def load_and_scale_image(path, scale_factor):  # function to load sprites
    image = pygame.image.load(path).convert_alpha()  # load image
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))  # return image

def run_pygame_splash_screen(image_path="./splash/img/pygame_powered_logo.png", scale_factor=0.3, timer_duration=3000):
    pygame.init()

    game_resolution = (800, 600)
    window = pygame.display.set_mode(game_resolution, pygame.DOUBLEBUF, 24)
    image = load_and_scale_image(image_path, scale_factor)
    start_ticks = pygame.time.get_ticks() 
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  

        elapsed_time = pygame.time.get_ticks() - start_ticks

        if elapsed_time >= timer_duration:
            print("Timer complete. Loading next scene.")

            time.sleep(1)  
            
            running = False 

        window.fill((0, 0, 0))  
        window.blit(image, (170, 200))  
        
        pygame.display.update()

