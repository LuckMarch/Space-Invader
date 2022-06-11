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


class player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = Yellow_Space_Ship
        self.laser_img = Yellow_Laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health




def main():
    Run = True
    FPS = 60
    Level = 1
    Lives = 5

    player_vel = 5

    Player = player(300, 650)
    clock = pygame.time.Clock()
    Main_Font = pygame.font.SysFont('comicsans', 30)

    def Redraw_Window():
        Win.blit(BG, (0, 0))
        # Draw text
        Lives_Label = Main_Font.render(f'Lives : {Lives}', 1, (255, 255, 255))
        Level_Label = Main_Font.render(f'Level : {Level}', 1, (255, 255, 255))
        Win.blit(Lives_Label, (10, 10))
        Win.blit(Level_Label, (Width - Lives_Label.get_width() - 10, 10))

        Player.draw(Win)
        pygame.display.update()

    while Run:
        clock.tick(FPS)
        Redraw_Window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and Player.x - player_vel > 0:  # Left
            Player.x -= player_vel
        if keys[pygame.K_RIGHT] and Player.x + player_vel + 50 < Width:  # Right
            Player.x += player_vel
        if keys[pygame.K_UP] and Player.y - player_vel > 0:  # Up
            Player.y -= player_vel
        if keys[pygame.K_DOWN] and Player.y + player_vel + 50 < Height:  # Down
            Player.y += player_vel

main()
