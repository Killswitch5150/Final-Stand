import pygame, sys, random, sounds
from settings import GameSettings, ScaleSettings  
from pygame.locals import *
from variables import *

console_debugging = False #change this to True to enable debugging log in console

last_reload_time = 0
reload_delay = 1500
shoot_delay = 500
reload_completion_time = 0
reloaderrors_spam = False 

clock = pygame.time.Clock() #to implement frame limit

#sound functions
def sound_reloading():
    sounds.reloading.set_volume(sounds.default_volume)
    pygame.mixer.Sound.play(sounds.reloading)
    if console_debugging: #debug output
        print('sound reloading playing')
    pygame.mixer.music.stop()

def sound_shooting():
    sounds.shooting.set_volume(sounds.default_volume)
    pygame.mixer.Sound.play(sounds.shooting)
    if console_debugging: #debug output
        print('sound shooting playing')
    pygame.mixer.music.stop()

#function defs
def create_tiling():
    for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

def create_road():
    #window.blit(spr_road_top, (200, 300))
    for x in range(0, 800, road_top_width):
        window.blit(spr_road_top, (x, 300))
    for x in range(0, 800, road_bottom_width):
        window.blit(spr_road_bottom, (x, 332))

def render_environment():
            #draw world elements for the background
            window.blit(spr_tree_image, (192, 64))
            window.blit(spr_tree_image, (192, 96))
            window.blit(spr_tree_image, (192, 128))
            window.blit(spr_tree_image, (192, 448))
            window.blit(spr_tree_image, (192, 480))
            window.blit(spr_tree_image, (192, 512))
            create_road()
            

def screen_size(): #function used by the full screen toggling function
    global screen_size_choice_fullscreen, flags, window #access global vars
    if screen_size_choice_fullscreen == True: 
        if console_debugging: #debug output
            print(f'fullscreen toggle set to {screen_size_choice_fullscreen}')
        flags = FULLSCREEN | DOUBLEBUF #define full screen vars
        window = pygame.display.set_mode(game_resolution, flags, 24) #set window to full screen
    if screen_size_choice_fullscreen == False:
        if console_debugging: #debug output
            print(f'fullscreen toggle set to off {screen_size_choice_fullscreen}')
        window = pygame.display.set_mode(game_resolution, pygame.DOUBLEBUF, 24) #set window to game_resolution size 

def toggle_fullscreen(): #function to toggle between fullscreen and windowed mode
    global screen_size_choice_fullscreen, window #access global vars
    screen_size_choice_fullscreen = not screen_size_choice_fullscreen #if fullscreen is true, make it false and vice-versa
    if console_debugging: #debug output
            print('fullscreen toggling')
    screen_size() #call screen_size function to initiate changes to window size

def load_and_scale_image(path, scale_factor): #function to load sprites
    if console_debugging: #debug output
            print('loading and scaling images')
    image = pygame.image.load(path).convert_alpha() #load image
    if console_debugging: #debug output
            print('complete')
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))) #return image and necessary variables

def load_images(): #function to load game images
    #make global vars accessible
    global tile_image, spr_player_image, spr_player_shooting_image, spr_road_top, spr_road_bottom, spr_player_shooting_mf_image, spr_tree_image, spr_enemy_image, spr_player_bullet, spr_ammo_image 
    if console_debugging: #debug output
            print('fetching assets')
    #define and provide paths to game assets to be loaded and scales
    tile_image = load_and_scale_image("sprites/grass.png", scaling.normal)
    spr_player_image = load_and_scale_image("sprites/player.png", scaling.double)
    spr_player_shooting_image = load_and_scale_image("sprites/player_shooting.png", scaling.double)
    spr_player_shooting_mf_image = load_and_scale_image("sprites/player_shooting_mf.png", scaling.double)
    spr_tree_image = load_and_scale_image("sprites/tree.png", scaling.normal)
    spr_enemy_image = load_and_scale_image("sprites/enemy.png", scaling.normal)
    spr_player_bullet = load_and_scale_image("sprites/projectile.png", scaling.half)
    spr_ammo_image = load_and_scale_image("sprites/ammo.png", scaling.normal)
    spr_road_top = load_and_scale_image("sprites/road.png", scaling.normal)
    spr_road_bottom_sprite = load_and_scale_image("sprites/road.png", scaling.normal)
    spr_road_bottom = pygame.transform.rotate(spr_road_bottom_sprite, -180.0)
    if console_debugging: #debug output
            print('assets fetched')

def get_stats(): #function to calculate widths and heights
    #make global vars accessible
    global tile_width, tile_height, player_width, player_height, road_top_height, road_top_width, road_bottom_height, road_bottom_width

    #define width and height vars
    if console_debugging: #debug output
            print('calculating heights and widths')
    tile_width = tile_image.get_width() 
    tile_height = tile_image.get_height()
    player_width = spr_player_image.get_width()
    player_height = spr_player_image.get_height()
    road_top_height = spr_road_top.get_height()
    road_top_width = spr_road_top.get_width()
    road_bottom_height = spr_road_bottom.get_height()
    road_bottom_width = spr_road_bottom.get_width()
    if console_debugging: #debug output
            print('heights and widths calculated')

def reset_game(settings): #function to reset tracked game vars
        global bullets, enemies, ammo_boxes #access necessary global vars
        bullets = [] #set bullets list to empty
        enemies = [] #set enemies list to empty
        ammo_boxes = [] #set ammo boxes list to empty

        #reset settings
        settings.kill_count = 0 #set kill count to zero
        settings.current_wave = 1 #set wave to one
        if console_debugging: #debug output
            print(f'game stats reset. {bullets} bullets, {enemies} enemies, {ammo_boxes}, ammo boxes')
            print(f'kill count: {settings.kill_count}, current wave: {settings.current_wave}')

def spawn_points_init():
    global enemy_spawn_points, ammo_spawn_points

    #define enemy spawn points
    enemy_spawn_points = [
        (width, random.randint(0, height - 50)),
        (width, random.randint(0, height - 50)),
        (width, random.randint(0, height - 50)),
    ]
    if console_debugging: #debug output
            print('enemy spawn points set')

    #define ammo box spawn points
    ammo_spawn_points = [
        (128, 96),
        (128, 480),
    ]
    if console_debugging: #debug output
            print('ammo spawn points set')
#end function defs

#class defs
class ReloadErrors:
    def draw(self, surface):
        import gui_text_vals
        messageisvisible = True

        #while messageisvisible:
        #    surface.blit(gui_text_vals.reloadinprogresstext_cantshoot, (width // 2 - gui_text_vals.reloadingtext_empty.get_width() // 2, height // 4))
        #    current_time3 = pygame.time.get_ticks()
        #    msg_delay = 1000
        #    if current_time3 >= msg_delay:
        #        messageisvisible = False

    
class InputHandler: #handle 'Global' game key inputs (accessible anywhere in the game)
    def __init__(self):
        self.fullscreen_key = pygame.K_F11 #set the full screen toggle key to F11

    def handle_input(self):
        for event in pygame.event.get(): #read events
            if event.type == pygame.QUIT: #if user quits
                if console_debugging: #debug output
                    print('user triggered quit')
                return "QUIT" #return quit value to controller

            if event.type == pygame.KEYDOWN: #read keydown events
                if event.key == self.fullscreen_key: #if F11 is pressed down
                    if console_debugging: #debug output
                        print('user triggered fullscreen toggle')
                    toggle_fullscreen() #execute the full screen toggle function

        return None  #return none if input is invalid

class ReloadControl:
    def __init__(self):
        self.needstoreload = True

    def update(self, surface, has_ammo):
        import gui_text_vals
        if has_ammo:
            window.blit(gui_text_vals.reloadingtext, (width // 2 - gui_text_vals.reloadingtext.get_width() // 2, height // 4))
        if not has_ammo:
            window.blit(gui_text_vals.reloadingtext_empty, (width // 2 - gui_text_vals.reloadingtext_empty.get_width() // 2, height // 4))

class GameOver: #class to define end of game events
    def __init__(self, settings):
        self.settings = settings 
        self.font_large = pygame.font.Font(None, 74) #larger font for end game GUI
        self.font_small = pygame.font.Font(None, 30) #smaller font for end game GUI
        
    def display(self, surface):
        import game_fonts

        surface.fill((0, 0, 0)) #black background

        kill_eval_var = GameOver.evaluate_kills(self, settings.kill_count) #pass settings and kill count to evaluate_kills function to define kill eval variable
        if console_debugging: #debug output
            print('kill_eval_var set')
        
        #defining GUI elements
        game_over_text = game_fonts.font.render("Game Over.", True, (255, 0, 0))
        kill_eval_text = game_fonts.font2.render(f"Kills: {settings.kill_count}. You are: {kill_eval_var}", True, (255, 0, 0))
        restart_text = game_fonts.font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        #draw GUI elements to the screen
        surface.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        surface.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        surface.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
        
        #display updated screen for the player
        pygame.display.flip()

        #read player input
        GameOver.handle_input(self)

    def evaluate_kills(self, kills): #defines the value to be stores in the kill eval variable 
        if console_debugging: #debug output
            print('evaluate_kills function running')
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
                        if console_debugging: #debug output
                            print('user triggered game restart')
                        return "RESTART" #return restart value
                    if event.key == pygame.K_q or pygame.K_ESCAPE: #if player hits Q or ESC key
                        if console_debugging: #debug output
                            print('user triggered quit game')
                        return "QUIT" #return quit value
            return None #return none if input is invalid 

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
            self.ammo_count -= 1 #reduce ammo_count by 1 per shot
            if console_debugging: #debug output
                print('bullet created')
                print(f'ammo_count: {self.ammo_count}')
        
    def draw(self, surface): #broken method intended for shooting animation
        if self.is_shooting: #if player is shooting
            surface.blit(self.shooting_image, self.rect.topleft) #change player sprite
            if console_debugging: #debug output
                print('player is shooting.')
        else: #if player is not shooting
            surface.blit(self.image, self.rect.topleft) #use the not shooting sprite

class Bullet: #bullet class
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        original_bullet_width, original_bullet_height = spr_player_bullet.get_size()  #scaling down bullet
        self.image = pygame.transform.scale(spr_player_bullet, (int(original_bullet_width * 0.5), int(original_bullet_height * 0.5)))  #scaling bullet down
        self.rect = self.image.get_rect(topleft=(x, y))  #create rectangle based on sprite dimensions
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4  #set speed
        
    def update(self, x, y):
        self.rect.x += self.speed  #bullet moves to the right when created
        #self.x = x
        #self.y = y  
        #print(f"bullet at {self.x}, {self.y}")
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  #instructions to create bullet

class Enemy: #enemy class
    def __init__(self, x, y, settings):
        #initialize enemies
        self.x = x 
        self.y = y
        original_enemy_width, original_enemy_height = spr_enemy_image.get_size()
        self.image = pygame.transform.scale(spr_enemy_image, (int(original_enemy_width * 2), int(original_enemy_height * 2)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        #define enemy speed by wave
        wave_speed_mapping = [0.6, 0.9, 2.0, 2.5, 3, 4, 6, 8, 10, 12.5, 15] 
        #enemy speed increases based on wave
        self.speed = wave_speed_mapping[settings.current_wave] if settings.current_wave < len(wave_speed_mapping) else 2    

    def update(self, x, y):
        #move left when spawned
        self.rect.x -= self.speed #move left when spawned at the defined speed
        #self.x = x 
        #self.y = y 
        #print(f"enemy at {self.x}, {self.y}")

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
#end class defs

#begin scene funcs
def game_over_screen(settings): #function to handle the game over screen
    import game_fonts, gui_text_vals

    eval_output = GameOver.evaluate_kills(GameOver, settings.kill_count)

    while True: #loop to play until player exits game over screen

        window.fill((0, 0, 0)) #black background
        
        #define UI element variables for the game over display
        kill_eval_text = game_fonts.font2.render(f"Kills: {settings.kill_count}. You are: {eval_output}", True, (255, 0, 0))
    

        #draw UI elements to the game over screen
        window.blit(gui_text_vals.game_over_text, (width // 2 - gui_text_vals.game_over_text.get_width() // 2, height // 4))
        window.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        window.blit(gui_text_vals.restart_text, (width // 2 - gui_text_vals.restart_text.get_width() // 2, height // 2))

        #draw the display to the player
        pygame.display.flip()

        #event handling
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits
                main_menu() #return to main menu
                if console_debugging: #debug output
                    print('user triggered quit')
            if event.type == pygame.KEYDOWN: #listen to key press
                if event.key == pygame.K_F11: #if player presses F11
                    if console_debugging: #debug output
                        print('player pressed F11')
                    toggle_fullscreen() #execute the full screen toggle function
                elif event.key == pygame.K_r: #if player presses R key
                    if console_debugging: #debug output
                        print('player pressed R')
                        print('tracked vars being reset and game restarted')
                    reset_game(settings) #reset the game values stored in settings
                    main(settings) #restart main function (game)
                elif event.key == pygame.K_q or pygame.K_ESCAPE: #if player hits Q or ESC
                    if console_debugging: #debug output
                        print('player pressed Q or ESC')
                    main_menu() #exit back to the main menu

def main_menu(): #main menu function
    import game_fonts, gui_text_vals
    #define variables for the main menu 

    button_rect = pygame.Rect(width // 2 - 100, height // 1.5 - 10, 200, 40) #define rectangle for button1 (play button)
    button2_rect = pygame.Rect(width // 2 - 100, height // 2 - 10, 200, 40) #define rectangle for button2 (controls button)

    running = True #enables running loop to begin

    while running: 
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits
                if console_debugging: #debug output
                    print('player triggered quit')
                pygame.quit() #quit
                sys.exit() #if nothing to quit, exit the program
            if event.type == pygame.MOUSEBUTTONDOWN: #listen for mouse clicks
                if button_rect.collidepoint(event.pos): #if player clicks on play button
                    if console_debugging: #debug output
                        print('player clicked on play button')
                    main(settings) #execute main function (start game)
                if button2_rect.collidepoint(event.pos): #if player clicks on controls button
                    if console_debugging: #debug output
                        print('player clicked on controls button')
                    mm_controls() #show game controls by executing mm_controls function
            if event.type == pygame.KEYDOWN: #listen for key presses
                if event.key == pygame.K_ESCAPE: #if player presses escape
                    if console_debugging: #debug output
                        print('player triggered quit with ESC')
                    pygame.quit() #quit
                    sys.exit() #if nothing to quit, exit the program
                if event.key == pygame.K_F11: #if player presses F11
                    if console_debugging: #debug output
                        print('player pressed F11')
                    toggle_fullscreen() #execute the fullscreen toggling function

        create_tiling() #creates the background
        render_environment() #creates the game world

        #drawing UI elements
        title_text = game_fonts.font.render(varGameName, True, (255, 0, 0)) #use varGameName for the main menu screen
        window.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3)) #draw game title on screen
        pygame.draw.rect(window, gui_text_vals.button_color_dark, button_rect) #create play button
        pygame.draw.rect(window, gui_text_vals.button_color_dark, button2_rect) #create controls button
        text_rect = gui_text_vals.text.get_rect(center=button_rect.center) #create object out of label
        text2_rect = gui_text_vals.text2.get_rect(center=button2_rect.center) #create object out of label
        window.blit(gui_text_vals.text, text_rect) #draw play text and button to window
        window.blit(gui_text_vals.text2, text2_rect) #draw controls text and button to window
        window.blit(spr_player_image, (width // 5 - player_width // 2, height // 2 - player_height // 2)) #draw player to window
        
        pygame.display.flip() #show the screen to the player

def mm_controls(): #function to control the controls screen
    import game_fonts, gui_text_vals

    #define the rectangle position and dimensions for the back button
    button1_rect = pygame.Rect(width // 2 - 50, height // 1.5 - 10, 100, 40)

    running = True #state control for the loop

    while running: #mm_controls loop
        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if player quits window
                if console_debugging: #debug output
                    print('player triggered quit')
                main_menu() #return to main menu
            if event.type == pygame.MOUSEBUTTONDOWN: #listen for mouse click
                if button1_rect.collidepoint(event.pos):  #if player clicks on button rectangle
                    if console_debugging: #debug output
                        print('player clicked back')
                    main_menu()  #return to main menu
            if event.type == pygame.KEYDOWN: #key press listener  
                if event.key == pygame.K_ESCAPE: #if player presses escape
                    if console_debugging: #debug output
                        print('player pressed ESC')
                    main_menu() #return to main menu
                if event.key == pygame.K_F11: #if player presses F11 key
                    if console_debugging: #debug output
                        print('player pressed F11')
                    toggle_fullscreen() #execute the fullscreen toggling function

        create_tiling() #creates the background

        #drawing text displays to the screen
        window.blit(gui_text_vals.title_text1, (width // 2 - gui_text_vals.title_text1.get_width() // 2, height // 5))
        window.blit(gui_text_vals.title_text2, (width // 2 - gui_text_vals.title_text2.get_width() // 2, height // 4))
        window.blit(gui_text_vals.title_text3, (width // 2 - gui_text_vals.title_text3.get_width() // 2, height // 3))
        window.blit(gui_text_vals.title_text4, (width // 2 - gui_text_vals.title_text4.get_width() // 2, height // 2))
        window.blit(gui_text_vals.title_text5, (width // 2 - gui_text_vals.title_text5.get_width() // 2, height // 2 - 50))
        
        pygame.draw.rect(window, gui_text_vals.button1_color_dark, button1_rect) #define the back buttons rectangle

        text_rect = gui_text_vals.text.get_rect(center=button1_rect.center) #create object for back button rectangle
        
        #draw the back button the screen
        window.blit(gui_text_vals.backtext, text_rect)

        #display the screen to the user
        pygame.display.flip()

def main(settings): #function to handle the main game loop
    import game_fonts
    
    reset_game(settings) #reset the games tracked variables whenever main loop is called

    #create the player object
    player = Player(settings.width // 5 - player_width // 2, settings.height // 2 - player_height // 2)
    
    #define variables for game logic
    occupied_positions = set() #create set to prevent RAM overload from too many spawns of ammo boxes
    ammo_drop_spawn_timer = 0 #spawn timer placeholder variable for initialization
    ammo_drop_spawn_interval = 100000 #spawn timer placeholder variable for initialization
    enemy_spawn_timer = 0 #enemy timer placeholder variable for initialization

    running = True #allows main loop to execute

    while running:
        #main game loop
        dt = clock.tick(60) #limit to 60 fps 

        wave_kills = settings.kill_count #define wave kills
        
        if settings.kill_count >= 10 * settings.current_wave: #every 10 kills
            if console_debugging:
                print(f"Wave {settings.current_wave + 1} is beginning") #debugging code
            settings.current_wave += 1 #increase wave by one
    
        #ensure maximum defined wave number can not be passsed
        if settings.current_wave > len(settings.waves):
            settings.current_wave = len(settings.waves)  #cap to maximum wave

        #set enemy spawn rate based on current wave
        if settings.current_wave > 0: #executes the entire time
            enemy_spawn_interval = settings.waves[settings.current_wave - 1]['enemy_spawn_rate']
            ammo_drop_spawn_interval = settings.waves[settings.current_wave - 1]['ammo_spawn_rate']

        current_time2 = pygame.time.get_ticks()

        for event in pygame.event.get(): #event listener
            if event.type == pygame.QUIT: #if user quits the window
                if console_debugging: #debug output
                    print('player triggered quit')
                running = False #game is no longer running
            if event.type == pygame.KEYDOWN: #key press listener
                if event.key == pygame.K_SPACE and player.ammo_count > 0: #if user hits space bar and has ammo
                    global reload_completion_time
                    if console_debugging: #debug output
                        print('player triggered shoot')
                    if current_time2 - reload_completion_time >= shoot_delay:
                        sound_shooting()
                        player.shoot() #execute the shoot method from the player class
                    elif current_time2 - reload_completion_time < shoot_delay:
                        global reloaderrors_spam
                        if console_debugging:
                            print('you cant shoot while reloading')
                        reloaderrors_spam = True 
                        
                if event.key == pygame.K_ESCAPE: #if user hits escape key
                    if console_debugging: #debug output
                        print('player pressed ESC')
                    game_over_screen(settings) #show the game over screen
                if event.key == pygame.K_F11: #if user hits the F11 key
                    if console_debugging: #debug output
                        print('player pressed F11')
                    toggle_fullscreen() #execute the fullscreen toggling function

        keys = pygame.key.get_pressed() #reading key presses / key bindings
        player.is_sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] #if Lshift or Rshift then issprinting becomes true
        if player.is_sprinting and console_debugging:
            print('player is sprinting')

        player.update() #while game is looping, repeatedly execute update method of player class
        
        if keys[pygame.K_r]: #if the user presses the R key
            if console_debugging: #debug output
                    print('player pressed R')
            if player.ammo_reserve > 0 and player.ammo_count < settings.player_magazine_size: #if player can shoot
                global last_reload_time, reload_delay
                #calculate how many rounds to reload
                current_time = pygame.time.get_ticks()
                rounds_to_reload = min(settings.player_magazine_size - player.ammo_count, player.ammo_reserve)  # Calculate how many rounds needed to fill the magazine
                #update ammo_count and ammo_reserve variables
                
                if current_time - last_reload_time >= reload_delay:
                    if console_debugging: #debug output
                        print('playing reload sound')
                        print('reloading')
                    sound_reloading()
                    player.ammo_count += rounds_to_reload
                    player.ammo_reserve -= rounds_to_reload
                    last_reload_time = current_time
                    reload_completion_time = current_time

        #updating bullet positions
        for bullet in bullets[:]:  #use a copy of the list to avoid unwanted modifications
            bullet.update(player.x, player.y) #execute bullet class update method
            bullet.draw(window) #create bullet on game surface
            
            if bullet.rect.x > settings.width: #if bullet leaves playable area (screen)
                bullets.remove(bullet) #remove the bullet
                if console_debugging: #debug output
                    print('bullet obj went off scree and was removed')
            else: #if bullet remains on screen
                bullet.draw(window) #draw the bullet object on the screen

        #enemy spawning logic
        enemy_spawn_timer += dt #increment timer
        if enemy_spawn_timer > settings.enemy_spawn_interval: #if enemy is ready to be spawned
            spawn_point = random.choice(enemy_spawn_points) #choose a spawn point from the list of spawn points
            enemies.append(Enemy(*spawn_point, settings)) #create an object of the class enemy and pass spawn point and settings values
            enemy_spawn_timer = 0 #restart spawn timer
            if console_debugging: #debug output
                    print('enemy spawned')
                    print(f'enemy respawn timer set to {enemy_spawn_timer}')

        #update enemies and check for collisions
        for enemy in enemies[:]:  #using a copy of the enemies list
            enemy.update(enemy.x, enemy.y) #execute the update method of the enemy class
            if enemy.rect.x < 0: #if enemy goes off screen
                enemies.remove(enemy) #remove the enemy from the game
                player.health -= 10 #remove 10 health from the player
                if console_debugging: #debug output
                    print('enemy made it to the end of player side')
        
            #bullet collision logic
            for bullet in bullets[:]:  #using a copy of the bullets list
                if bullet.rect.colliderect(enemy.rect): #if bullet collides with enemy
                    bullets.remove(bullet) #remove bullet object
                    enemies.remove(enemy) #remove enemy object
                    settings.kill_count += 1 #add one to kill count
                    if console_debugging: #debug output
                        print('bullet and enemy collision detected')
                        print(f'kills: {settings.kill_count}')
                    break #ensure if statement does not execute multiple times per kill. should be redundant and unneccessary
                #offset_x, offset_y = int(enemy.update() - bullet.x), int(enemy.y - bullet.y)
                #if bullet.mask.overlap(enemy.mask, (offset_x, offset_y)): #if bullet collides with enemy
                #    print("offset")
                #    bullets.remove(bullet) #remove bullet object
                #    enemies.remove(enemy) #remove enemy object
                #    settings.kill_count += 1 #add one to kill count
                #    break #ensure if statement does not execute multiple times per kill. should be redundant and unneccessary
                
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
                    if console_debugging: #debug output
                        print('ammo box spawned')
                attempts += 1 #add one to attempts if ammo box can not spawn

        for ammo in ammo_boxes[:]: #using a copy of ammo box lists
            if ammo.rect.colliderect(player.rect): #if player collides with ammo box
                    ammo_boxes.remove(ammo) #remove the object instance of ammo box
                    occupied_positions.remove(ammo.rect.topleft) #remove ammo box from occupied positions
                    possible_ammo_drops = [12, 12, 12, 12, 24, 24, 24, 36, 36, 48, 72] #define ammo amounts possible in ammo drops (repeats to increase probability)
                    ammo_drop_size_decider = random.choice(possible_ammo_drops)
                    player.ammo_reserve += ammo_drop_size_decider #add the amount from ammo drop to the player's ammo reserve
                    if console_debugging: #debug output
                        print('ammo box and player collision detected')
                        print(f'player picked up {ammo_drop_size_decider} ammo')
                    break #should be redundant, ensures system wont execute this multiple times per ammo drop
        
        if not ammo_boxes: #if there are no ammo boxes
            occupied_positions.clear() #clears the positions variable to free up space for new ones
            
        if player.health <= 0: #if player health is zero
            if console_debugging: #debug output
                    print('player has died')
            game_over_screen(settings) #show the game over screen

        create_tiling() #creates the background
        render_environment() #creates the game world
        player.draw(window) #creates the player

        #reloading gui logic
        if player.ammo_count == 0:
            if player.ammo_reserve > 0:
                has_ammo = True
            elif player.ammo_reserve == 0:
                has_ammo = False
            reloadingalert = ReloadControl
            reloadingalert.update(reloadingalert, window, has_ammo)
            if console_debugging:    
                print('player needs to reload')
                print('reload message displaying')
        if reloaderrors_spam:
            ReloadErrors_obj.draw(ReloadErrors, window)
    
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
        health_text = game_fonts.guifont.render(f"Health: {player.health}", True, (255, 0, 0))
        kill_text = game_fonts.guifont.render(f"Kills: {settings.kill_count}", True, (255, 0, 0))
        ammo_text = game_fonts.guifont.render(f"Ammo: {player.ammo_count} / {player.ammo_reserve}", True, (255, 0, 0))
        current_wave = settings.current_wave
        current_wave_text = game_fonts.guifont.render(f"Wave: {current_wave}", True, (255, 0, 0))
        window.blit(health_text, (10, 10))
        window.blit(ammo_text, (10, 40))
        window.blit(kill_text, (width // 2 - kill_text.get_width() // 2, 10))
        window.blit(current_wave_text, (width // 2 - kill_text.get_width() // 2, 40))

        #display the screen to the player
        pygame.display.flip()

#define init objects
settings = GameSettings() #create settings obj
scaling = ScaleSettings() #define scaling from ScaleSettings class (imported)
ReloadErrors_obj = ReloadErrors

#run init functions
load_images() #execute load_images function
get_stats() #execute function to define size vars
spawn_points_init() #initiate function to define spawn points

#scene load order
main_menu()  #when game launches, start at the main menu
pygame.quit()
pygame.mixer.stop() #should be redundant. ensures sound doesn't continue to attempt to play
sys.exit()
