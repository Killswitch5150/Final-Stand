import pygame  
import sys 
import random #for spawners 

#testing git
#testing branching

varGameName = "Final Stand"

# Initiating pygame and variables
pygame.init()
pygame.display.set_caption(varGameName)
width, height = 800, 600  # window size vars
window = pygame.display.set_mode((width, height))  # window size
bullet_ready_to_shoot = True
bullets, enemies, ammo_boxes = []
player_health, kill_count = 100, 0

# Loading assets
tile_image = pygame.image.load("sprites/grass.png")  # load grass sprite
tile_width, tile_height = tile_image.get_size()  # sprite dimensions
spr_player_image = pygame.image.load("sprites/player.png")  # load player sprite
spr_player_width, spr_player_height = spr_player_image.get_size()  # player dimensions
spr_player_shooting_image = pygame.image.load("sprites/player_shooting.png")  # load player sprite
spr_player_shooting_width, spr_player_shooting_height = spr_player_shooting_image.get_size()  # player dimensions
spr_player_shooting_mf_image = pygame.image.load("sprites/player_shooting_mf.png")  # load player sprite
spr_player_shooting_mf_width, spr_player_shooting_mf_height = spr_player_shooting_mf_image.get_size()  # player dimensions
spr_tree_image = pygame.image.load("sprites/tree.png")  # load tree sprite
spr_tree_width, spr_tree_height = spr_tree_image.get_size()  # tree size
spr_enemy_image = pygame.image.load("sprites/enemy.png")  # load enemy sprite
spr_enemy_width, spr_enemy_height = spr_enemy_image.get_size()  # enemy size
spr_player_bullet = pygame.image.load("sprites/projectile.png")  # load projectile
spr_player_bullet_width, spr_player_bullet_height = spr_player_bullet.get_size()  # projectile size
spr_ammo_image = pygame.image.load("sprites/ammo.png") #load ammo sprite
spr_ammo_width, spr_ammo_height = spr_ammo_image.get_size() #ammo size

#spr_enemy_rect = spr_enemy_image.get_rect()
#spr_enemy_mask = pygame.mask.from_surface(spr_enemy_image)
#spr_enemy_mask_image = spr_enemy_mask.to_surface()


# Scaling player
scaled_player_image = pygame.transform.scale(spr_player_image, (spr_player_width * 2, spr_player_height * 2))
scaled_player_width, scaled_player_height = scaled_player_image.get_size()
scaled_player_shooting_image = pygame.transform.scale(spr_player_shooting_image, (spr_player_shooting_width * 2, spr_player_shooting_height * 2))
scaled_player_shooting_width, scaled_player_shooting_height = scaled_player_shooting_image.get_size()
scaled_player_shooting_mf_image = pygame.transform.scale(spr_player_shooting_mf_image, (spr_player_shooting_mf_width * 2, spr_player_shooting_mf_height * 2))
scaled_player_shooting_mf_width, scaled_player_shooting_mf_height = scaled_player_shooting_mf_image.get_size()

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
    def __init__(self, x, y):
        original_enemy_width, original_enemy_height = spr_enemy_image.get_size()
        self.image = pygame.transform.scale(spr_enemy_image, (int(original_enemy_width * 2), int(original_enemy_height * 2)))
        self.rect = self.image.get_rect(topleft=(x, y))
        try:
            if wave1:
                self.speed = 0.6  # enemy speed
            elif wave2:
                self.speed = 0.9
            elif wave3:
                self.speed = 2.0
            elif wave4:
                self.speed = 2.5
            elif wave5:
                self.speed = 3
            elif wave6:
                self.speed = 4
        except:
            self.speed = 2
            

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

def game_over_screen():
    while True:
        window.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 30)
        kill_eval_var = "deficiency"

        if kill_count < 10:
            kill_eval_var = "A No Go At This Lane"
        elif kill_count >= 10 and kill_count < 25:
            kill_eval_var = "Trash"
        elif kill_count >= 25 and kill_count < 50:
            kill_eval_var = "Insubordinate"
        elif kill_count >= 50 and kill_count < 75:
            kill_eval_var = "F.N.G."
        elif kill_count >= 75 and kill_count < 100:
            kill_eval_var = "Pretty Good"
        elif kill_count >= 100:
            kill_eval_var = "Get A Life"

        game_over_text = font.render(f"Game Over.", True, (255, 0, 0))
        kill_eval_text = font2.render(f"Kills: {kill_count}. You are: {kill_eval_var}", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

        window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        window.blit(kill_eval_text, (width // 2 - kill_eval_text.get_width() // 2, height // 3))
        window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))

        pygame.display.flip()

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
        window.blit(scaled_player_image, (width // 5 - scaled_player_width // 2, height // 2 - scaled_player_height // 2))
        
        pygame.display.flip()

def mm_controls():
    running = True 
    button1_color_dark = (100, 100, 100)
    button1_color_light = (254, 254, 0)
    button1_rect = pygame.Rect(width // 2 - 50, height // 1.5 - 10, 100, 40)  # Centered button

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
    global player_health, player_speed, player_isshooting, wave1, wave2, wave3, wave4, wave5, wave6, wave_kills, enemy_wave, kill_count, bullets, enemies, ready_to_spawn, ammo_count, ammo_reserve

    # Reset game state
    player_health = 100
    player_isshooting = False
    kill_count = 0
    wave_kills = 0
    switch_wave = False 
    bullets = []
    enemies = []
    ammo_boxes = []
    max_ammo_boxes = 2
    ammo_count = 7 #rounds in mag
    ammo_reserve = 0 #rounds not in mag
    player_can_reload = True
    occupied_positions = set()
    ammo_drop_spawn_timer = 0
    ammo_drop_spawn_interval = 10000 
    enemy_spawn_timer = 0
    enemy_wave = 1
    enemy_spawn_interval = 1500  # Changed to 1500 milliseconds (1.5 seconds)
    ready_to_spawn = True #flag to prevent overspawning
    
    # Initializing positions
    player_x = width // 5 - scaled_player_width // 2
    player_y = height // 2 - scaled_player_height // 2
    player_speed = 3.5  # Player speed
    player_issprinting = False 

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

        wave_kills = kill_count
        

        if kill_count == 10 and wave1 == True:
            enemy_spawn_interval = 1500
            ammo_drop_spawn_interval = 10000
            enemy_wave += 1
            print(f"Wave {enemy_wave} is beginning")
            wave1 = False
            wave2 = True
            
        if kill_count == 25 and wave2 == True:
            enemy_spawn_interval = wave2enemyspawnrate
            ammo_drop_spawn_interval = wave2ammospawnrate
            enemy_wave += 1
            print(f"Wave {enemy_wave} is beginning")
            wave2 = False
            wave3 = True
        
        if kill_count == 50 and wave3 == True:
            enemy_spawn_interval = wave3enemyspawnrate
            ammo_drop_spawn_interval = wave3ammospawnrate
            enemy_wave += 1
            print(f"Wave {enemy_wave} is beginning")
            wave3 = False
            wave4 = True

        if kill_count == 75 and wave4 == True:
            enemy_spawn_interval = wave4enemyspawnrate
            ammo_drop_spawn_interval = wave4ammospawnrate
            enemy_wave += 1
            print(f"Wave {enemy_wave} is beginning")
            wave4 = False
            wave5 = True    

        if kill_count == 100 and wave5 == True:
            enemy_spawn_interval = wave5enemyspawnrate
            ammo_drop_spawn_interval = wave5ammospawnrate
            enemy_wave += 1
            print(f"Wave {enemy_wave} is beginning")
            wave5 = False
            wave6 = True

        for event in pygame.event.get(): #allows user to quit the game
            if event.type == pygame.QUIT:
                running = False 
    
        if not player_issprinting:
            speed = 3.5

        if player_issprinting:
            speed = 5
            print(f'sprinting: {player_issprinting}')

        #reading key presses / key bindings
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= speed 
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                player_issprinting = True
                #print(f'sprinting: {player_issprinting}')
            if not keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                player_issprinting = False
                #print(f'sprinting: {player_issprinting}')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += speed 
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                player_issprinting = True
                #print(f'sprinting: {player_issprinting}')
            if not keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                player_issprinting = False
                #print(f'sprinting: {player_issprinting}')


        if keys[pygame.K_SPACE] and bullet_ready_to_shoot and ammo_count >= 1:
            bullet = Bullet(player_x + scaled_player_width, player_y + scaled_player_height // 2)
            bullets.append(bullet)
            player_isshooting = True
            bullet_ready_to_shoot = False
            ammo_count -= 1
        if not keys[pygame.K_SPACE]:
            player_isshooting = False
            bullet_ready_to_shoot = True
        
        if keys[pygame.K_r]:
            if ammo_reserve > 0 and ammo_count < 7:
                # Calculate how many rounds to reload
                rounds_to_reload = min(7 - ammo_count, ammo_reserve)  # Calculate how many rounds needed to fill the magazine
                # Update ammo_count and ammo_reserve
                ammo_count += rounds_to_reload
                ammo_reserve -= rounds_to_reload
            # Ensure ammo_count does not exceed 7 (this check is now redundant but can stay for safety)
            if ammo_count > 7:
                ammo_count = 7

        # Updating bullet positions
        for bullet in bullets[:]:  # Use a copy of the list to avoid modifying it while iterating
            bullet.update()
            # Remove bullet if it goes off screen
            if bullet.rect.x > width:
                bullets.remove(bullet)

        # Spawning enemies
        enemy_spawn_timer += dt # Increment timer
        if enemy_spawn_timer > enemy_spawn_interval:
            spawn_point = random.choice(enemy_spawn_points)
            enemies.append(Enemy(*spawn_point))
            enemy_spawn_timer = 0

        # Update enemies and check for collisions
        for enemy in enemies[:]:  # Use a copy of the list for safe removal
            enemy.update()
            # Remove enemy if it goes off screen
            if enemy.rect.x < 0:
                enemies.remove(enemy)
                player_health -= 10
        
            # Check for collision with bullets
            for bullet in bullets[:]:  # Use a copy of the list for safe removal
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    kill_count += 1
                    break
            #if enemy.rect.colliderect(pygame.Rect(player_x, player_y, 1, 1)):
             #   enemies.remove(enemy)
              #  kill_count += 1
                
        ammo_drop_spawn_timer += dt  # Increment timer
        if ammo_drop_spawn_timer > ammo_drop_spawn_interval:
            if len(ammo_boxes) < max_ammo_boxes:
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
            if ammo.rect.colliderect(pygame.Rect(player_x, player_y, scaled_player_width, scaled_player_height)):
                    ammo_boxes.remove(ammo)
                    occupied_positions.remove(ammo.rect.topleft)
                    ammo_reserve += 21
                    break
        
        if not ammo_boxes:
            occupied_positions.clear()

        if player_health <= 0:
            game_over_screen()

        #if player_isshooting:
         #   window.blit(spr_player_shooting_mf_image, (player_x, player_y))
        #if not player_isshooting:
         #   window.blit(spr_player_shooting_image, (player_x, player_y))

        if player_y < 0:
            player_y = 0
        if player_y > height - scaled_player_height:
            player_y = height - scaled_player_height

        for x in range(0, width, tile_width):
            for y in range(0, height, tile_height):
                window.blit(tile_image, (x, y))

        #drawing the game objects
        window.blit(scaled_player_image, (player_x, player_y))
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
        health_text = font.render(f"Health: {player_health}", True, (255, 0, 0))
        kill_text = font.render(f"Kills: {kill_count}", True, (255, 0, 0))
        ammo_text = font.render(f"Ammo: {ammo_count} / {ammo_reserve}", True, (255, 0, 0))
        window.blit(health_text, (10, 10))
        window.blit(kill_text, (width // 2 - kill_text.get_width() // 2, 10))
        window.blit(ammo_text, (width // 1.5 - ammo_text.get_width() // 2, 10))
   
        pygame.display.flip()

main_menu()  # Show the main menu first
pygame.quit()
sys.exit()
