import pygame
#game settings and image settings

class ScaleSettings:
    def __init__(self):
        self.normal = 1
        self.double = 2
        self.half = 0.5
        #new vars can be added to accomodate different scaling

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
        self.current_wave = 1

        #wave settings
        self.waves = [
            {'enemy_spawn_rate': 1000, 'ammo_spawn_rate': 15000},
            {'enemy_spawn_rate': 800, 'ammo_spawn_rate': 16000},
            {'enemy_spawn_rate': 500, 'ammo_spawn_rate': 17500},
            {'enemy_spawn_rate': 250, 'ammo_spawn_rate': 20000},
            {'enemy_spawn_rate': 200, 'ammo_spawn_rate': 22500},
            {'enemy_spawn_rate': 150, 'ammo_spawn_rate': 25000},
            {'enemy_spawn_rate': 100, 'ammo_spawn_rate': 27500},
            {'enemy_spawn_rate': 75, 'ammo_spawn_rate': 30000},
            {'enemy_spawn_rate': 50, 'ammo_spawn_rate': 32500},
            {'enemy_spawn_rate': 25, 'ammo_spawn_rate': 35000}
        ]
        
