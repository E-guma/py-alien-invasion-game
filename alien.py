"""This Module contains the class 'Alien' to control alien behaviours
   for Alien Invasion"""
   
from os import path
import pygame
from pygame.sprite import Sprite   

# Get the alien image file path
current_path = path.dirname(__file__)
image_path = path.join(current_path, 'images', 'alien.bmp')

class Alien(Sprite):
    """A class to model a single alien in the fleet."""
    def __init__(self, settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_frect()
        
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Update Alien's position"""
        self.rect.x += self.settings.alien_speed_factor * self.settings.fleet_direction


