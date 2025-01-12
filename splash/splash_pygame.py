import pygame
import time  # Optional, for simulating a script execution delay if needed

def load_and_scale_image(path, scale_factor):  # function to load sprites
    image = pygame.image.load(path).convert_alpha()  # load image
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))  # return image

def run_pygame_splash_screen(image_path="./splash/img/pygame_powered_logo.png", scale_factor=0.3, timer_duration=3000):
    """
    Runs the splash screen with a 5-second timer.

    Args:
    - image_path (str): Path to the splash image.
    - scale_factor (float): The scale factor for resizing the image.
    - timer_duration (int): Duration of the timer in milliseconds (default is 5000ms or 5 seconds).
    """
    pygame.init()  # Initialize Pygame

    
    #game_resolution = (960, 540)  # Set game resolution
    game_resolution = (800, 600)  # Set game resolution
    window = pygame.display.set_mode(game_resolution, pygame.DOUBLEBUF, 24)  # Create the window

    # Load and scale the image
    image = load_and_scale_image(image_path, scale_factor)

    # Start the timer
    start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit if the window is closed

        # Get the elapsed time
        elapsed_time = pygame.time.get_ticks() - start_ticks

        # Execute a different script or action when the timer expires (5 seconds)
        if elapsed_time >= timer_duration:
            print("5 seconds have passed! Executing the next script...")

            # Example: Execute additional code here
            # For example, simulate executing another script or function
            time.sleep(1)  # Simulate script execution with a 1-second delay (optional)
            print("Additional actions executed after timer.")
            
            # Exit the loop once the timer finishes
            running = False  # Stop the game loop after the timer is done

        # Blit the image to the screen
        window.fill((0, 0, 0))  # Clear the screen with black
        window.blit(image, (170, 200))  # Draw the image at position (100, 100)
        
        # Update the display
        pygame.display.update()

    # Quit Pygame
    #pygame.quit()
