import pygame  
import sys 
import random #for spawners 

varGameName = "Final Stand"

#initiating pygame, setting up window settings and vars
pygame.init()
pygame.display.set_caption(varGameName)
width, height = 800, 600  # window size vars
window = pygame.display.set_mode((width, height))  # window size
bullet_ready_to_shoot = True
bullets, enemies, ammo_boxes = [], [], []

def load_and_scale_image(path, scale_factor): #function to load sprites
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

class GameOver:
    def __init__(self, settings):
        self.settings = settings 
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 30)
    
    def display(self, surface):
        surface.fill((0, 0, 0))

        kill_eval_var = self.evaluate_kills(self.settings.kill_count)

        game_over_text = self.font_large.render("Game Over.", True, (255, 0, 0))
        kill_eval_text = self.font_small.render(f"Kills: {self.settings.kill_count}. You are: {kill_eval_var}", True, (255, 0, 0))
        restart_text = self.font_large.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        surface.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        surface.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        surface.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))
        
        pygame.display.flip()  # Update the display

        self.handle_input()

    def evaluate_kills(self, kills):
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
    
    def handle_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

class ScaleSettings:
    def __init__(self):
        self.normal = 1
        self.double = 2
        self.half = 0.5
        #new vars can be added to accomodate different scaling

scaling = ScaleSettings()

def load_images():
    global tile_image, spr_player_image, spr_player_shooting_image, spr_player_shooting_mf_image, spr_tree_image, spr_enemy_image, spr_player_bullet, spr_ammo_image
    tile_image = load_and_scale_image("sprites/grass.png", scaling.normal) #loading sprites and scaling
    spr_player_image = load_and_scale_image("sprites/player.png", scaling.double)
    spr_player_shooting_image = load_and_scale_image("sprites/player_shooting.png", scaling.double)
    spr_player_shooting_mf_image = load_and_scale_image("sprites/player_shooting_mf.png", scaling.double)
    spr_tree_image = load_and_scale_image("sprites/tree.png", scaling.normal)
    spr_enemy_image = load_and_scale_image("sprites/enemy.png", scaling.normal)
    spr_player_bullet = load_and_scale_image("sprites/projectile.png", scaling.half)
    spr_ammo_image = load_and_scale_image("sprites/ammo.png", scaling.normal)

load_images()

tile_width = tile_image.get_width() #getting sizes for collisions and tiling
tile_height = tile_image.get_height()
player_width = spr_player_image.get_width()
player_height = spr_player_image.get_height()

class GameSettings:
    def __init__(self):
        self.game_name = "Final Stand"
        self.width = 800
        self.height = 600
        self.player_magazine_size = 24
        self.ammo_drop_size = 48
        self.enemy_spawn_interval = 1500
        self.ammo_drop_spawn_interval = 10000
        self.max_ammo_boxes = 2
        self.kill_count = 0

        #wave settings
        self.waves = [
            {'enemy_spawn_rate': 1000, 'ammo_spawn_rate': 15000},
            {'enemy_spawn_rate': 800, 'ammo_spawn_rate': 16000},
            {'enemy_spawn_rate': 500, 'ammo_spawn_rate': 17500},
            {'enemy_spawn_rate': 250, 'ammo_spawn_rate': 20000}
        ]
        self.current_wave = 0

class Player:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.health = 100
        self.ammo_count = 24
        self.ammo_reserve = 0
        self.is_shooting = False
        self.is_sprinting = False 
        self.speed = 3.5

        #loading player sprite
        self.image = load_and_scale_image("sprites/player.png", 2)
        self.shooting_image = load_and_scale_image("sprites/player_shooting.png", 2)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))

    def update(self):
        #update position based on player input
        keys = pygame.key.get_pressed()
        speed = self.speed + 1.5 if self.is_sprinting else self.speed

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
        
    def shoot(self):
        if self.ammo_count > 0:
            bullet = Bullet(self.rect.right, self.rect.centery)
            bullets.append(bullet)
            print("Bullet created")
            self.ammo_count -= 1
        
    def draw(self, surface):
        if self.is_shooting:
            surface.blit(self.shooting_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

class Bullet:
    def __init__(self, x, y):
        original_bullet_width, original_bullet_height = spr_player_bullet.get_size()  # scaling down bullet
        self.image = pygame.transform.scale(spr_player_bullet, (int(original_bullet_width * 0.5), int(original_bullet_height * 0.5)))  # scaling bullet down
        self.rect = self.image.get_rect(topleft=(x, y))  # create rectangle based on sprite dimensions
        self.speed = 4  # set speed
        
    def update(self):
        self.rect.x += self.speed  # Bullet moves to the right when created
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # instructions to create bullet

class Enemy:
    def __init__(self, x, y, settings):
        original_enemy_width, original_enemy_height = spr_enemy_image.get_size()
        self.image = pygame.transform.scale(spr_enemy_image, (int(original_enemy_width * 2), int(original_enemy_height * 2)))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        wave_speed_mapping = [0.6, 0.9, 2.0, 2.5, 3, 4]
        self.speed = wave_speed_mapping[settings.current_wave] if settings.current_wave < len(wave_speed_mapping) else 2    

    def update(self):
        # Move left when spawned
        self.rect.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Ammo:
    def __init__(self, x, y):
        original_ammo_width, original_ammo_height = spr_ammo_image.get_size()
        self.image = pygame.transform.scale(spr_ammo_image, (int(original_ammo_width), int(original_ammo_height)))
        self.rect = self.image.get_rect(topleft=(x, y))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

enemy_spawn_points = [
    (width, random.randint(0, height - 50)),
    (width, random.randint(0, height - 50)),
    (width, random.randint(0, height - 50)),
]

ammo_spawn_points = [
    (128, 96),
    (128, 480),
]

def reset_game(settings):
        global bullets, enemies, ammo_boxes
        bullets = []
        enemies = []
        ammo_boxes = []

        #reset settings
        settings.kill_count = 0
        settings.current_wave = 0

def game_over_screen(settings):
    
    while True:
        window.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 30)
        kill_eval_var = "deficiency"

        if settings.kill_count < 10:
            kill_eval_var = "A No Go At This Lane"
        elif settings.kill_count >= 10 and settings.kill_count < 25:
            kill_eval_var = "Trash"
        elif settings.kill_count >= 25 and settings.kill_count < 50:
            kill_eval_var = "Insubordinate"
        elif settings.kill_count >= 50 and settings.kill_count < 75:
            kill_eval_var = "F.N.G."
        elif settings.kill_count >= 75 and settings.kill_count < 100:
            kill_eval_var = "Pretty Good"
        elif settings.kill_count >= 100:
            kill_eval_var = "Get A Life"

        game_over_text = font.render(f"Game Over.", True, (255, 0, 0))
        kill_eval_text = font2.render(f"Kills: {settings.kill_count}. You are: {kill_eval_var}", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        window.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_r:
                    reset_game(settings)
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main_menu():
    running = True 
    button_color_dark = (100, 100, 100)
    button_color_light = (254, 254, 0)
    button_rect = pygame.Rect(width // 2 - 100, height // 1.5 - 10, 200, 40)  # Centered play button
    button2_rect = pygame.Rect(width // 2 - 100, height // 2 - 10, 200, 40)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Check if mouse is over the button
                    main()  # Start the game
                if button2_rect.collidepoint(event.pos):  # Check if mouse is over the button
                    mm_controls()  # Show controls

        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        window.blit(spr_tree_image, (192, 64))
        window.blit(spr_tree_image, (192, 96))
        window.blit(spr_tree_image, (192, 128))
        window.blit(spr_tree_image, (192, 448))
        window.blit(spr_tree_image, (192, 480))
        window.blit(spr_tree_image, (192, 512))

        font = pygame.font.Font(None, 74)
        title_text = font.render(varGameName, True, (255, 0, 0))
        window.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
        pygame.draw.rect(window, button_color_dark, button_rect)
        pygame.draw.rect(window, button_color_dark, button2_rect)
        smallfont = pygame.font.Font(None, 34) 
        text = smallfont.render('PLAY', True, button_color_light)
        text_rect = text.get_rect(center=button_rect.center)
        text2 = smallfont.render('CONTROLS', True, button_color_light)
        text2_rect = text2.get_rect(center=button2_rect.center)
        window.blit(text, text_rect)
        window.blit(text2, text2_rect)
        window.blit(spr_player_image, (width // 5 - player_width // 2, height // 2 - player_height // 2))
        
        pygame.display.flip()

def mm_controls():
    running = True 
    button1_color_dark = (100, 100, 100)
    button1_color_light = (254, 254, 0)
    button1_rect = pygame.Rect(width // 2 - 50, height // 1.5 - 10, 100, 40)  # Centered button

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):  # Check if mouse is over the button
                    main_menu()  #go back to main menu

        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        varControls = "Game Controls:"
        varGClineone = "Up/Down Arrow Keys or 'W' and 'S' keys to move"
        varGClinetwo = "'R' to reload"
        varGClinethree = "Spacebar to shoot"
        varGClinefour = "Ammo drops randomly spawn to give you more ammo"

        font = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 18)
        title_text1 = font.render(varControls, True, (255, 0, 0))
        title_text2 = font2.render(varGClineone, True, (255, 0, 0))
        title_text3 = font2.render(varGClinetwo, True, (255, 0, 0))
        title_text4 = font2.render(varGClinethree, True, (255, 0, 0))
        title_text5 = font2.render(varGClinefour, True, (255, 0, 0))
        window.blit(title_text1, (width // 2 - title_text1.get_width() // 2, height // 5))
        window.blit(title_text2, (width // 2 - title_text2.get_width() // 2, height // 4))
        window.blit(title_text3, (width // 2 - title_text3.get_width() // 2, height // 3))
        window.blit(title_text4, (width // 2 - title_text4.get_width() // 2, height // 2))
        window.blit(title_text5, (width // 2 - title_text5.get_width() // 2, height // 2 - 50))
        pygame.draw.rect(window, button1_color_dark, button1_rect)
        smallfont = pygame.font.Font(None, 34) 
        text = smallfont.render('BACK', True, button1_color_light)
        text_rect = text.get_rect(center=button1_rect.center)
        window.blit(text, text_rect)

        pygame.display.flip()

def main():
    settings = GameSettings()
    reset_game(settings)

    game_over = GameOver(settings)

    #create the player
    player = Player(settings.width // 5 - player_width // 2, settings.height // 2 - player_height // 2)
    
    player_isshooting = False
    occupied_positions = set()
    ammo_drop_spawn_timer = 0
    ammo_drop_spawn_interval = 10000 
    enemy_spawn_timer = 0
    enemy_wave = 1
    ready_to_spawn = True #flag to prevent overspawning

    running = True 
    clock = pygame.time.Clock() #to implement frame limit

    #setting flags to control waves
    wave1 = True
    wave2 = False
    wave3 = False
    wave4 = False
    wave5 = False
    wave6 = False 

    #setting spawn rate vars for waves
    wave2enemyspawnrate = 1000
    wave2ammospawnrate = 15000
    wave3enemyspawnrate = 800
    wave3ammospawnrate = 16000
    wave4enemyspawnrate = 500
    wave4ammospawnrate = 17500
    wave5enemyspawnrate = 250
    wave5ammospawnrate = 20000


    while running:
        dt = clock.tick(60) #limit to 60 fps

        wave_kills = settings.kill_count
        
        if settings.kill_count >= (settings.current_wave + 1) * 10 and settings.current_wave < len(settings.waves):
            print(f"Wave {settings.current_wave + 1} is beginning")
            settings.current_wave += 1  # Move to the next wave
        
        if settings.current_wave > 0:
            enemy_spawn_interval = settings.waves[settings.current_wave - 1]['enemy_spawn_rate']
            ammo_drop_spawn_interval = settings.waves[settings.current_wave - 1]['ammo_spawn_rate']

        for event in pygame.event.get(): #allows user to quit the game
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.ammo_count > 0:
                    player.shoot() 

        #reading key presses / key bindings
        keys = pygame.key.get_pressed()
        player.is_sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_LSHIFT]
        
        player.update()

        if player.is_shooting:
            player.shoot()
        
        if keys[pygame.K_r]:
            if player.ammo_reserve > 0 and player.ammo_count < settings.player_magazine_size:
                # Calculate how many rounds to reload
                rounds_to_reload = min(settings.player_magazine_size - player.ammo_count, player.ammo_reserve)  # Calculate how many rounds needed to fill the magazine
                # Update ammo_count and ammo_reserve
                player.ammo_count += rounds_to_reload
                player.ammo_reserve -= rounds_to_reload
            # Ensure ammo_count does not exceed 7 (this check is now redundant but can stay for safety)
            if player.ammo_count > settings.player_magazine_size:
                player.ammo_count = settings.player_magazine_size

        # Updating bullet positions
        for bullet in bullets[:]:  # Use a copy of the list to avoid modifying it while iterating
            bullet.update()
            bullet.draw(window)
            # Remove bullet if it goes off screen
            if bullet.rect.x > settings.width:
                bullets.remove(bullet)
            else:
                bullet.draw(window)

        # Spawning enemies
        enemy_spawn_timer += dt # Increment timer
        if enemy_spawn_timer > settings.enemy_spawn_interval:
            spawn_point = random.choice(enemy_spawn_points)
            enemies.append(Enemy(*spawn_point, settings))
            enemy_spawn_timer = 0

        # Update enemies and check for collisions
        for enemy in enemies[:]:  # Use a copy of the list for safe removal
            enemy.update()
            # Remove enemy if it goes off screen
            if enemy.rect.x < 0:
                enemies.remove(enemy)
                player.health -= 10
        
            # Check for collision with bullets
            for bullet in bullets[:]:  # Use a copy of the list for safe removal
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    settings.kill_count += 1
                    break
                
        ammo_drop_spawn_timer += dt  # Increment timer
        if ammo_drop_spawn_timer > settings.ammo_drop_spawn_interval:
            if len(ammo_boxes) < settings.max_ammo_boxes:
                max_attempts = 10
                attempts = 0
                spawn_successful = False

            while attempts < max_attempts and not spawn_successful:
                spawn_point = random.choice(ammo_spawn_points)
                if spawn_point not in occupied_positions:
                    ammo_boxes.append(Ammo(*spawn_point))
                    occupied_positions.add(spawn_point)
                    ammo_drop_spawn_timer = 0
                    spawn_successful = True 
                attempts += 1

        for ammo in ammo_boxes[:]:
            if ammo.rect.colliderect(player.rect):
                    ammo_boxes.remove(ammo)
                    occupied_positions.remove(ammo.rect.topleft)
                    player.ammo_reserve += settings.ammo_drop_size
                    break
        
        if not ammo_boxes:
            occupied_positions.clear()

        if player.health <= 0:
            #game_over_screen(settings)
            game_over.display(window)
            reset_game(settings)
            continue

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

         # Draw health and kill count GUI
        font = pygame.font.Font(None, 36)  # Creates a font object
        health_text = font.render(f"Health: {player.health}", True, (255, 0, 0))
        kill_text = font.render(f"Kills: {settings.kill_count}", True, (255, 0, 0))
        ammo_text = font.render(f"Ammo: {player.ammo_count} / {player.ammo_reserve}", True, (255, 0, 0))
        window.blit(health_text, (10, 10))
        window.blit(kill_text, (width // 2 - kill_text.get_width() // 2, 10))
        window.blit(ammo_text, (width // 1.5 - ammo_text.get_width() // 2, 10))
   
        pygame.display.flip()

main_menu()  # Show the main menu first
pygame.quit()
sys.exit()
