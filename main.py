import pygame
import os
import time
import random
import Object_Classes as OC
pygame.font.init()
Ship = OC.Ship

# Window
Width, Height = 750, 750
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Space Invader')

# Load Enemy Ship
Red_Space_Ship = OC.load('assets', 'pixel_ship_red_small.png')
Green_Space_Ship = OC.load('assets', 'pixel_ship_green_small.png')
Blue_Space_Ship = OC.load('assets', 'pixel_ship_blue_small.png')
# Load Player Ship
Yellow_Space_Ship = OC.load('assets', 'pixel_ship_yellow.png')

# Load Laser
Red_Laser = OC.load('assets', 'pixel_laser_red.png')
Green_Laser = OC.load('assets', 'pixel_laser_green.png')
Blue_Laser = OC.load('assets', 'pixel_laser_blue.png')
Yellow_Laser = OC.load('assets', 'pixel_laser_yellow.png')

# Load Background
BG = pygame.transform.scale(OC.load('assets', 'background-black.png'), (Width, Height))

# Classes
class player(Ship):
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = Yellow_Space_Ship
        self.laser_img = Yellow_Laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown(self)
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(Height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


class Enemy(Ship):
    Color_Map = {
        'red': (Red_Space_Ship, Red_Laser),
        'green': (Green_Space_Ship, Green_Laser),
        'blue': (Blue_Space_Ship, Blue_Laser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.Color_Map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel




def main():
    Run = True
    Lost = False
    Lost_Count = 0
    FPS = 60
    Level = 0
    Lives = 5

    enemies = []
    wave_length= 5
    enemy_vel = 1
    laser_vel = 4

    player_vel = 5

    Player = player(300, 650)

    clock = pygame.time.Clock()
    Main_Font = pygame.font.SysFont('comicsans', 30)
    Lost_Font = pygame.font.SysFont('comicsans', 50, True)

    def Redraw_Window():
        Win.blit(BG, (0, 0))

        # Draw Enemies
        for enemy in enemies:
            enemy.draw(Win)

        Player.draw(Win)

        # Draw text
        Lives_Label = Main_Font.render(f'Lives : {Lives}', 1, (255, 255, 255))
        Level_Label = Main_Font.render(f'Level : {Level}', 1, (255, 255, 255))
        Win.blit(Lives_Label, (10, 10))
        Win.blit(Level_Label, (Width - Lives_Label.get_width() - 10, 10))

        if Lost:
            lost_label = Lost_Font.render('GAME OVER', 1, (255, 255, 255))
            Win.blit(lost_label, (Width/2  - lost_label.get_width()/2, 350))

        pygame.display.update()

    while Run:
        clock.tick(FPS)
        Redraw_Window()

        if Lives <= 0 or Player.health <= 0:
            Lost = True
            Lost_Count += 1

        if Lost:
            if Lost_Count > FPS * 5:
                Run = False
            else:
                continue


        if len(enemies) == 0:
            Level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, Width - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and Player.x - player_vel > 0:  # Left
            Player.x -= player_vel
        if keys[pygame.K_RIGHT] and Player.x + player_vel + Player.get_width() < Width:  # Right
            Player.x += player_vel
        if keys[pygame.K_UP] and Player.y - player_vel > 0:  # Up
            Player.y -= player_vel
        if keys[pygame.K_DOWN] and Player.y + player_vel + Player.get_height() < Height:  # Down
            Player.y += player_vel
        if keys[pygame.K_SPACE]:
            Player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if enemy.y + enemy.get_height() > Height:
                Lives -= 1
                enemies.remove(enemy)

        player.move_lasers(player, laser_vel, enemies)

main()
