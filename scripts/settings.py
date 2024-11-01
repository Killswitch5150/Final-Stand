import pygame 
#game settings and image settings

class ScaleSettings: #create ScaleSettings class
    def __init__(self):
        self.normal = 1
        self.double = 2
        self.half = 0.5
        #new vars can be added to accomodate different scaling

class GameSettings: #create GameSettings class
    def __init__(self):
        self.game_name = "Final Stand" #game name
        self.width = 800 #window width
        self.height = 600 #window height
        self.player_magazine_size = 24 #max amount of ammo player can have loaded at once
        self.enemy_spawn_interval = 1500 #placeholder enemy spawn interval for initialization
        self.ammo_drop_spawn_interval = 10000 #placeholder ammo drop spawn interval for initialization
        self.max_ammo_boxes = 2 #maximum amount of ammo boxes that can be in the game at the same time
        self.kill_count = 0 #game starts with zero kills
        self.current_wave = 1 #game starts at wave 1

        #wave settings
        self.waves = [
            {'enemy_spawn_rate': 1000, 'ammo_spawn_rate': 20000},
            {'enemy_spawn_rate': 800, 'ammo_spawn_rate': 22500},
            {'enemy_spawn_rate': 500, 'ammo_spawn_rate': 25000},
            {'enemy_spawn_rate': 250, 'ammo_spawn_rate': 27500},
            {'enemy_spawn_rate': 200, 'ammo_spawn_rate': 30000},
            {'enemy_spawn_rate': 150, 'ammo_spawn_rate': 32500},
            {'enemy_spawn_rate': 100, 'ammo_spawn_rate': 35000},
            {'enemy_spawn_rate': 75, 'ammo_spawn_rate': 40000},
            {'enemy_spawn_rate': 50, 'ammo_spawn_rate': 45000},
            {'enemy_spawn_rate': 25, 'ammo_spawn_rate': 50000}
        ]
        
