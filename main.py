import pygame  
import sys
from settings import GameSettings, ScaleSettings 
import random #for spawners 
from pygame.locals import *

settings = GameSettings() #create settings obj

screen_size_choice_fullscreen = False #default value for fullscreen toggle

varGameName = "Final Stand" #name of the game to appear on window and UI

#initiating pygame, setting up window settings and vars
pygame.mixer.pre_init(44100, 16, 2, 4096) #initializing audio support
pygame.init() #initiating pygame 
pygame.display.set_caption(varGameName) #set window text to name of the game
width, height = 800, 600  # window size vars
game_resolution = (width, height) #put window size tuple into game_resolution var
window = pygame.display.set_mode((game_resolution), pygame.DOUBLEBUF, 24)  # window size set to game res
bullet_ready_to_shoot = True #starts playing with shooting action enabled
bullets, enemies, ammo_boxes = [], [], [] #declares empty lists to be written during gameplay

def screen_size(): #function used by the full screen toggling function
    global screen_size_choice_fullscreen, flags, window #access global vars
    if screen_size_choice_fullscreen == True: 
        flags = FULLSCREEN | DOUBLEBUF #define full screen vars
        window = pygame.display.set_mode(game_resolution, flags, 24) #set window to full screen
    if screen_size_choice_fullscreen == False:
        window = pygame.display.set_mode(game_resolution, pygame.DOUBLEBUF, 24) #set window to game_resolution size 

def toggle_fullscreen(): #function to toggle between fullscreen and windowed mode
    global screen_size_choice_fullscreen, window #access global vars
    screen_size_choice_fullscreen = not screen_size_choice_fullscreen #if fullscreen is true, make it false and vice-versa
    screen_size() #call screen_size function to initiate changes to window size


def load_and_scale_image(path, scale_factor): #function to load sprites
    image = pygame.image.load(path).convert_alpha() #load image
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))) #return image and necessary variables

class InputHandler: #handle 'Global' game key inputs (accessible anywhere in the game)
    def __init__(self):
        self.fullscreen_key = pygame.K_F11 #set the full screen toggle key to F11

    def handle_input(self):
        for event in pygame.event.get(): #read events
            if event.type == pygame.QUIT: #if user quits
                return "QUIT" #return quit value to controller

            if event.type == pygame.KEYDOWN: #read keydown events
                if event.key == self.fullscreen_key: #if F11 is pressed down
                    toggle_fullscreen() #execute the full screen toggle function

        return None  #return none if input is invalid

class GameOver: #class to define end of game events
    def __init__(self, settings):
        self.settings = settings 
        self.font_large = pygame.font.Font(None, 74) #larger font for end game GUI
        self.font_small = pygame.font.Font(None, 30) #smaller font for end game GUI
    
    def display(self, surface):
        surface.fill((0, 0, 0)) #black background

        kill_eval_var = self.evaluate_kills(self.settings.kill_count) #pass settings and kill count to evaluate_kills function to define kill eval variable

        #defining GUI elements
        game_over_text = self.font_large.render("Game Over.", True, (255, 0, 0))
        kill_eval_text = self.font_small.render(f"Kills: {self.settings.kill_count}. You are: {kill_eval_var}", True, (255, 0, 0))
        restart_text = self.font_large.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        #draw GUI elements to the screen
        surface.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        surface.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        surface.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
        
        #display updated screen for the player
        pygame.display.flip()

        #read player input
        self.handle_input()

    def evaluate_kills(self, kills): #defines the value to be stores in the kill eval variable 
        if kills < 10:
            return "A No Go At This Lane"
        elif kills < 25:
            return "Trash"
        elif kills < 50:
            return "Insubordinate"
        elif kills < 75:
            return "F.N.G."
        elif kills < 100:
            return "Pretty Good"
        else:
            return "Get A Life"
    
    def handle_input(self): #function to handle input
        while True: #loop while input handling is active
            for event in pygame.event.get(): #read events
                if event.type == pygame.QUIT: #if player quits
                    pygame.quit() #quit game
                if event.type == pygame.KEYDOWN: #read key input
                    if event.key == pygame.K_r: #if player hits R key
                        return "RESTART" #return restart value
                    if event.key == pygame.K_q or pygame.K_ESCAPE: #if player hits Q or ESC key
                        return "QUIT" #return quit value
            return None #return none if input is invalid 

scaling = ScaleSettings() #define scaling from ScaleSettings class (imported)

def load_images(): #function to load game images
    #make global vars accessible
    global tile_image, spr_player_image, spr_player_shooting_image, spr_player_shooting_mf_image, spr_tree_image, spr_enemy_image, spr_player_bullet, spr_ammo_image 
    
    #define and provide paths to game assets to be loaded and scales
    tile_image = load_and_scale_image("sprites/grass.png", scaling.normal)
    spr_player_image = load_and_scale_image("sprites/player.png", scaling.double)
    spr_player_shooting_image = load_and_scale_image("sprites/player_shooting.png", scaling.double)
    spr_player_shooting_mf_image = load_and_scale_image("sprites/player_shooting_mf.png", scaling.double)
    spr_tree_image = load_and_scale_image("sprites/tree.png", scaling.normal)
    spr_enemy_image = load_and_scale_image("sprites/enemy.png", scaling.normal)
    spr_player_bullet = load_and_scale_image("sprites/projectile.png", scaling.half)
    spr_ammo_image = load_and_scale_image("sprites/ammo.png", scaling.normal)

load_images() #execute load_images function

def get_stats(): #function to calculate widths and heights
    #make global vars accessible
    global tile_width, tile_height, player_width, player_height

    #define width and height vars
    tile_width = tile_image.get_width() 
    tile_height = tile_image.get_height()
    player_width = spr_player_image.get_width()
    player_height = spr_player_image.get_height()

get_stats() #execute function to define size vars

class Player: #player class
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.health = 100 #set player health
        self.ammo_count = 24 #set magazine size
        self.ammo_reserve = 0 #set ammo reserve starting count
        self.is_shooting = False #player does not spawn in shooting
        self.is_sprinting = False #player does not spawn in sprinting
        self.speed = 3.5 #set player speed

        #loading player sprite using load_and_scale_image function
        self.image = load_and_scale_image("sprites/player.png", 2)
        self.shooting_image = load_and_scale_image("sprites/player_shooting.png", 2)
        self.rect = self.image.get_rect(topleft=(self.x,self.y)) #define player collision box

    def update(self):
        #update position based on player input
        keys = pygame.key.get_pressed() #read key input
        speed = self.speed + 1.5 if self.is_sprinting else self.speed #player speed modification for sprinting

        #player movement logic
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            self.y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += speed
            
        #ensure player stays on screen
        if self.y < 0:
            self.y = 0
        if self.y > height - self.rect.height:
            self.y = height - self.rect.height

        self.rect.topleft = (self.x, self.y)
        
    def shoot(self): #shooting method
        if self.ammo_count > 0: #check if player has ammo
            bullet = Bullet(self.rect.right, self.rect.centery) #create bullet
            bullets.append(bullet) #add bullet to bullet list
            print("Bullet created") #debugging code
            self.ammo_count -= 1 #reduce ammo_count by 1 per shot
        
    def draw(self, surface): #broken method intended for shooting animation
        if self.is_shooting: #if player is shooting
            surface.blit(self.shooting_image, self.rect.topleft) #change player sprite
        else: #if player is not shooting
            surface.blit(self.image, self.rect.topleft) #use the not shooting sprite

class Bullet: #bullet class
    def __init__(self, x, y):
        original_bullet_width, original_bullet_height = spr_player_bullet.get_size()  #scaling down bullet
        self.image = pygame.transform.scale(spr_player_bullet, (int(original_bullet_width * 0.5), int(original_bullet_height * 0.5)))  #scaling bullet down
        self.rect = self.image.get_rect(topleft=(x, y))  #create rectangle based on sprite dimensions
        self.speed = 4  #set speed
        
    def update(self):
        self.rect.x += self.speed  #bullet moves to the right when created
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  #instructions to create bullet

class Enemy: #enemy class
    def __init__(self, x, y, settings):
        #initialize enemies
        original_enemy_width, original_enemy_height = spr_enemy_image.get_size()
        self.image = pygame.transform.scale(spr_enemy_image, (int(original_enemy_width * 2), int(original_enemy_height * 2)))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        #define enemy speed by wave
        wave_speed_mapping = [0.6, 0.9, 2.0, 2.5, 3, 4, 6, 8, 10, 12.5, 15] 
        #enemy speed increases based on wave
        self.speed = wave_speed_mapping[settings.current_wave] if settings.current_wave < len(wave_speed_mapping) else 2    

    def update(self):
        #move left when spawned
        self.rect.x -= self.speed #move left when spawned at the defined speed

    def draw(self, surface):
        #draw the enemy
        surface.blit(self.image, self.rect.topleft)

class Ammo: #ammo class
    def __init__(self, x, y):
        #initialize ammo boxes
        original_ammo_width, original_ammo_height = spr_ammo_image.get_size()
        self.image = pygame.transform.scale(spr_ammo_image, (int(original_ammo_width), int(original_ammo_height)))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, surface):
        #draw ammo box to screen
        surface.blit(self.image, self.rect.topleft)

#define enemy spawn points
enemy_spawn_points = [
    (width, random.randint(0, height - 50)),
    (width, random.randint(0, height - 50)),
    (width, random.randint(0, height - 50)),
]

#define ammo box spawn points
ammo_spawn_points = [
    (128, 96),
    (128, 480),
]

def reset_game(settings): #function to reset tracked game vars
        global bullets, enemies, ammo_boxes #access necessary global vars
        bullets = [] #set bullets list to empty
        enemies = [] #set enemies list to empty
        ammo_boxes = [] #set ammo boxes list to empty

        #reset settings
        settings.kill_count = 0 #set kill count to zero
        settings.current_wave = 1 #set wave to one

def game_over_screen(settings): #function to handle the game over screen
    while True: #loop to play until player exits game over screen

        window.fill((0, 0, 0)) #black background
        font = pygame.font.Font(None, 74) #define font 
        font2 = pygame.font.Font(None, 30) #define font2
        
        #define UI element variables for the game over display
        game_over_text = font.render(f"Game Over.", True, (255, 0, 0)) 
        kill_eval_text = font2.render(f"Kills: {settings.kill_count}. You are: {GameOver.evaluate_kills(GameOver, kills=settings.kill_count)}", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        #draw UI elements to the game over screen
        window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        window.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))

        #draw the display to the player
        pygame.display.flip()

        #event handling
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits
                main_menu() #return to main menu
            if event.type == pygame.KEYDOWN: #listen to key press
                if event.key == pygame.K_F11: #if player presses F11
                    toggle_fullscreen() #execute the full screen toggle function
                elif event.key == pygame.K_r: #if player presses R key
                    reset_game(settings) #reset the game values stored in settings
                    main(settings) #restart main function (game)
                elif event.key == pygame.K_q or pygame.K_ESCAPE: #if player hits Q or ESC
                    main_menu() #exit back to the main menu

def main_menu(): #main menu function
    #define variables for the main menu 
    button_color_dark = (100, 100, 100) #define dark button color
    button_color_light = (254, 254, 0) #define light button color
    button_rect = pygame.Rect(width // 2 - 100, height // 1.5 - 10, 200, 40) #define rectangle for button1 (play button)
    button2_rect = pygame.Rect(width // 2 - 100, height // 2 - 10, 200, 40) #define rectangle for button2 (controls button)

    running = True #enables running loop to begin

    while running: 
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits
                pygame.quit() #quit
                sys.exit() #if nothing to quit, exit the program
            if event.type == pygame.MOUSEBUTTONDOWN: #listen for mouse clicks
                if button_rect.collidepoint(event.pos): #if player clicks on play button
                    main(settings) #execute main function (start game)
                if button2_rect.collidepoint(event.pos): #if player clicks on controls button
                    mm_controls() #show game controls by executing mm_controls function
            if event.type == pygame.KEYDOWN: #listen for key presses
                if event.key == pygame.K_ESCAPE: #if player presses escape
                    pygame.quit() #quit
                    sys.exit() #if nothing to quit, exit the program
                if event.key == pygame.K_F11: #if player presses F11
                    toggle_fullscreen() #execute the fullscreen toggling function

        #tile the tile_image to create a background
        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        #draw world elements for the background
        window.blit(spr_tree_image, (192, 64))
        window.blit(spr_tree_image, (192, 96))
        window.blit(spr_tree_image, (192, 128))
        window.blit(spr_tree_image, (192, 448))
        window.blit(spr_tree_image, (192, 480))
        window.blit(spr_tree_image, (192, 512))

        #drawing UI elements
        font = pygame.font.Font(None, 74) #define font for menu
        title_text = font.render(varGameName, True, (255, 0, 0)) #use varGameName for the main menu screen
        window.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3)) #draw game title on screen
        pygame.draw.rect(window, button_color_dark, button_rect) #create play button
        pygame.draw.rect(window, button_color_dark, button2_rect) #create controls button
        smallfont = pygame.font.Font(None, 34) #define smallfont for menu
        text = smallfont.render('PLAY', True, button_color_light) #create label for play button
        text_rect = text.get_rect(center=button_rect.center) #create object out of label
        text2 = smallfont.render('CONTROLS', True, button_color_light) #create label for controls button
        text2_rect = text2.get_rect(center=button2_rect.center) #create object out of label
        window.blit(text, text_rect) #draw play text and button to window
        window.blit(text2, text2_rect) #draw controls text and button to window
        window.blit(spr_player_image, (width // 5 - player_width // 2, height // 2 - player_height // 2)) #draw player to window
        
        pygame.display.flip() #show the screen to the player

def mm_controls(): #function to control the controls screen
    #define variables
    button1_color_dark = (100, 100, 100)
    button1_color_light = (254, 254, 0)

    #define the rectangle position and dimensions for the back button
    button1_rect = pygame.Rect(width // 2 - 50, height // 1.5 - 10, 100, 40)

    running = True #state control for the loop

    while running: #mm_controls loop
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits window
                main_menu() #return to main menu
            if event.type == pygame.MOUSEBUTTONDOWN: #listen for mouse click
                if button1_rect.collidepoint(event.pos):  #if player clicks on button rectangle
                    main_menu()  #return to main menu
            if event.type == pygame.KEYDOWN: #key press listener  
                if event.key == pygame.K_ESCAPE: #if player presses escape
                    main_menu() #return to main menu
                if event.key == pygame.K_F11: #if player presses F11 key
                    toggle_fullscreen() #execute the fullscreen toggling function

        #tiling for background display
        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        #defining text for UI
        varControls = "Game Controls:"
        varGClineone = "Up/Down Arrow Keys or 'W' and 'S' keys to move"
        varGClinetwo = "'R' to reload"
        varGClinethree = "Spacebar to shoot"
        varGClinefour = "Ammo drops randomly spawn to give you more ammo"

        #defining fonts
        font = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 18)
        smallfont = pygame.font.Font(None, 34)

        #creating text displays
        title_text1 = font.render(varControls, True, (255, 0, 0))
        title_text2 = font2.render(varGClineone, True, (255, 0, 0))
        title_text3 = font2.render(varGClinetwo, True, (255, 0, 0))
        title_text4 = font2.render(varGClinethree, True, (255, 0, 0))
        title_text5 = font2.render(varGClinefour, True, (255, 0, 0))

        #drawing text displays to the screen
        window.blit(title_text1, (width // 2 - title_text1.get_width() // 2, height // 5))
        window.blit(title_text2, (width // 2 - title_text2.get_width() // 2, height // 4))
        window.blit(title_text3, (width // 2 - title_text3.get_width() // 2, height // 3))
        window.blit(title_text4, (width // 2 - title_text4.get_width() // 2, height // 2))
        window.blit(title_text5, (width // 2 - title_text5.get_width() // 2, height // 2 - 50))
        
        pygame.draw.rect(window, button1_color_dark, button1_rect) #define the back buttons rectangle

        text = smallfont.render('BACK', True, button1_color_light) #create object for back button text
        text_rect = text.get_rect(center=button1_rect.center) #create object for back button rectangle
        
        #draw the back button the screen
        window.blit(text, text_rect)

        #display the screen to the user
        pygame.display.flip()

def main(settings): #function to handle the main game loop
    reset_game(settings) #reset the games tracked variables whenever main loop is called

    #create the player object
    player = Player(settings.width // 5 - player_width // 2, settings.height // 2 - player_height // 2)
    
    #define variables for game logic
    occupied_positions = set() #create set to prevent RAM overload from too many spawns of ammo boxes
    ammo_drop_spawn_timer = 0 #spawn timer placeholder variable for initialization
    ammo_drop_spawn_interval = 100000 #spawn timer placeholder variable for initialization
    enemy_spawn_timer = 0 #enemy timer placeholder variable for initialization

    running = True #allows main loop to execute

    clock = pygame.time.Clock() #to implement frame limit

    while running:
        #main game loop
        dt = clock.tick(60) #limit to 60 fps 

        wave_kills = settings.kill_count #define wave kills
        
        if settings.kill_count >= 10 * settings.current_wave: #every 10 kills
            print(f"Wave {settings.current_wave + 1} is beginning") #debugging code
            settings.current_wave += 1 #increase wave by one
    
        #ensure maximum defined wave number can not be passsed
        if settings.current_wave > len(settings.waves):
            settings.current_wave = len(settings.waves)  #cap to maximum wave

        #set enemy spawn rate based on current wave
        if settings.current_wave > 0: #executes the entire time
            enemy_spawn_interval = settings.waves[settings.current_wave - 1]['enemy_spawn_rate']
            ammo_drop_spawn_interval = settings.waves[settings.current_wave - 1]['ammo_spawn_rate']

        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if user quits the window
                running = False #game is no longer running
            if event.type == pygame.KEYDOWN: #key press listener
                if event.key == pygame.K_SPACE and player.ammo_count > 0: #if user hits space bar and has ammo
                    player.shoot() #execute the shoot method from the player class 
                if event.key == pygame.K_ESCAPE: #if user hits escape key
                    game_over_screen(settings) #show the game over screen
                if event.key == pygame.K_F11: #if user hits the F11 key
                    toggle_fullscreen() #execute the fullscreen toggling function

        keys = pygame.key.get_pressed() #reading key presses / key bindings
        player.is_sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] #if Lshift or Rshift then issprinting becomes true
        
        player.update() #while game is looping, repeatedly execute update method of player class

        if player.is_shooting: #if the player is shooting
            player.shoot() #execute the shoot method of the player class
        
        if keys[pygame.K_r]: #if the user presses the R key
            if player.ammo_reserve > 0 and player.ammo_count < settings.player_magazine_size: #if player can shoot
                #calculate how many rounds to reload
                rounds_to_reload = min(settings.player_magazine_size - player.ammo_count, player.ammo_reserve)  # Calculate how many rounds needed to fill the magazine
                #update ammo_count and ammo_reserve variables
                player.ammo_count += rounds_to_reload
                player.ammo_reserve -= rounds_to_reload

        #updating bullet positions
        for bullet in bullets[:]:  #use a copy of the list to avoid unwanted modifications
            bullet.update() #execute bullet class update method
            bullet.draw(window) #create bullet on game surface
            
            if bullet.rect.x > settings.width: #if bullet leaves playable area (screen)
                bullets.remove(bullet) #remove the bullet
            else: #if bullet remains on screen
                bullet.draw(window) #draw the bullet object on the screen

        #enemy spawning logic
        enemy_spawn_timer += dt #increment timer
        if enemy_spawn_timer > settings.enemy_spawn_interval: #if enemy is ready to be spawned
            spawn_point = random.choice(enemy_spawn_points) #choose a spawn point from the list of spawn points
            enemies.append(Enemy(*spawn_point, settings)) #create an object of the class enemy and pass spawn point and settings values
            enemy_spawn_timer = 0 #restart spawn timer

        #update enemies and check for collisions
        for enemy in enemies[:]:  #using a copy of the enemies list
            enemy.update() #execute the update method of the enemy class
            if enemy.rect.x < 0: #if enemy goes off screen
                enemies.remove(enemy) #remove the enemy from the game
                player.health -= 10 #remove 10 health from the player
        
            #bullet collision logic
            for bullet in bullets[:]:  #using a copy of the bullets list
                if bullet.rect.colliderect(enemy.rect): #if bullet collides with enemy
                    bullets.remove(bullet) #remove bullet object
                    enemies.remove(enemy) #remove enemy object
                    settings.kill_count += 1 #add one to kill count
                    break #ensure if statement does not execute multiple times per kill. should be redundant and unneccessary
                
        ammo_drop_spawn_timer += dt  #increment timer for ammo drop spawner
        if ammo_drop_spawn_timer > settings.ammo_drop_spawn_interval: #if ammo drop is ready to spawn
            if len(ammo_boxes) < settings.max_ammo_boxes: #prevent ammo boxes from overspawning
                #local variables for spawning system
                max_attempts = 10
                attempts = 0
                spawn_successful = False

            while attempts < max_attempts and not spawn_successful: #while ammo drop spawning is possible
                spawn_point = random.choice(ammo_spawn_points) #choose random spawn location for ammo drop from list of possible locations
                if spawn_point not in occupied_positions: #check if spawn point is unoccupied
                    ammo_boxes.append(Ammo(*spawn_point)) #create object of ammo class
                    occupied_positions.add(spawn_point) #tell spawning system the spawn location is occupied until player picks up the ammo drop
                    ammo_drop_spawn_timer = 0 #reset spawn timer
                    spawn_successful = True #managing state change
                attempts += 1 #add one to attempts if ammo box can not spawn

        for ammo in ammo_boxes[:]: #using a copy of ammo box lists
            if ammo.rect.colliderect(player.rect): #if player collides with ammo box
                    ammo_boxes.remove(ammo) #remove the object instance of ammo box
                    occupied_positions.remove(ammo.rect.topleft) #remove ammo box from occupied positions
                    player.ammo_reserve += settings.ammo_drop_size #add the amount from ammo drop to the player's ammo reserve
                    break #should be redundat, ensures system wont execute this multiple times per ammo drop
        
        if not ammo_boxes: #if there are no ammo boxes
            occupied_positions.clear() #clears the positions variable to free up space for new ones

        if player.health <= 0: #if player health is zero
            game_over_screen(window) #show the game over screen

        #draw tiled background
        for x in range(0, width, tile_width): 
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        #drawing the game objects
        player.draw(window) 
        window.blit(spr_tree_image, (192, 64))
        window.blit(spr_tree_image, (192, 96))
        window.blit(spr_tree_image, (192, 128))
        window.blit(spr_tree_image, (192, 448))
        window.blit(spr_tree_image, (192, 480))
        window.blit(spr_tree_image, (192, 512))
    
        #drawing bullets
        for bullet in bullets:
            bullet.draw(window)

        #drawing enemies
        for enemy in enemies:
            enemy.draw(window)

        #draw ammo boxes
        for ammo in ammo_boxes:
            ammo.draw(window)

        #draw health and kill count GUI
        font = pygame.font.Font(None, 36)  #define font
        health_text = font.render(f"Health: {player.health}", True, (255, 0, 0))
        kill_text = font.render(f"Kills: {settings.kill_count}", True, (255, 0, 0))
        ammo_text = font.render(f"Ammo: {player.ammo_count} / {player.ammo_reserve}", True, (255, 0, 0))
        current_wave = settings.current_wave
        current_wave_text = font.render(f"Wave: {current_wave}", True, (255, 0, 0))
        window.blit(health_text, (10, 10))
        window.blit(ammo_text, (10, 40))
        window.blit(kill_text, (width // 2 - kill_text.get_width() // 2, 10))
        window.blit(current_wave_text, (width // 2 - kill_text.get_width() // 2, 40))

        #display the screen to the player
        pygame.display.flip()

main_menu()  #when game launches, start at the main menu
pygame.quit()
sys.exit()
