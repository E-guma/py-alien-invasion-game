"""This Module contains the class 'Ship' to control ships behaviour
   for Alien Invasion"""
from os import path
import pygame

# Get the ship image file path
current_path = path.dirname(__file__)
image_path = path.join(current_path, 'images', 'ship.bmp')
    
class Ship(pygame.sprite.Sprite):
    """Methods and attributes for modelling ship behaviours"""
    
    def __init__(self, settings, screen):
        """initializing ship attributes"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        
        # Load the image into memory
        self.image = pygame.image.load(image_path).convert()
        # Get the image and screen rect for easy positioning 
        self.rect = self.image.get_frect()
        self.screen_rect = self.screen.get_frect()
        
        # Use the image rect to place it at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            self.rect.centerx += self.settings.ship_speed_factor
        if self.moving_left:
            self.rect.centerx -= self.settings.ship_speed_factor
        self.rect.clamp_ip(self.screen_rect)  # Ensure the ship stays within screen bounds
        
    def blitme(self):
        """Draws the ship at its current location."""
        self.screen.blit(self.image, self.rect)    
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.centerx = self.screen_rect.centerx


