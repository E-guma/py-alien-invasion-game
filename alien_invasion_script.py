# A L I E N   I N V A S I O N

import pygame
from pygame.sprite import Group
# Game Modules
import game_functions as gf
from game_stats import GameStats
from settings import Settings
from background import Background
from scoreboard import Scoreboard
from button import Button
from ship import Ship


def run_game():
    """Main function to run the Alien Invasion game."""
    # Initialize game and create a screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)
    clock = pygame.time.Clock()
    # Make the Play button.
    play_button = Button(settings, screen, "Play")
    # Create an instance to store game statistics
    stats = GameStats(settings)
    # Create a scoreboard
    sb = Scoreboard(settings, screen, stats)
    # Create the background
    bg = Background(settings, screen)
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(settings, screen) 
    bullets = Group()
    aliens = Group()
        
    # Create fleet of aliens
    gf.create_fleet(settings, screen, ship, aliens)    

    # Start the main loop for the game.
    while True: 
        # Watch for keyboard and mouse events.
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            # Update background, ship, bullets, and aliens positions
            bg.update()
            ship.update()  
            gf.update_bullets(settings, screen, stats, sb,   ship, aliens, bullets)
            gf.update_aliens(settings, stats, sb, screen, ship, aliens, bullets)
        
        # Update screen elements
        gf.update_screen(screen, settings, stats, sb, bg, ship, aliens, bullets, play_button)
        clock.tick(60)

run_game()

