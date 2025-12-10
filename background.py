"""This Module Manages the Background for the Alien Invasion Game."""

from os import path

import pygame

IMAGE_PATH = path.join(path.dirname(__file__), 'images', 'bg1.png')

class Background:
    """A class to manage the background image."""
    
    def __init__(self, settings, screen):
        """Initialize the background."""
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load(IMAGE_PATH).convert()
        self.image = pygame.transform.scale(self.image, 
                        (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.image.get_frect()
        self.rect.topleft = (0, 0)
    
    def update(self):
        """Update the background position for scrolling effect."""
        self.rect.y += self.settings.bg_scroll_speed
        if self.rect.y >= self.settings.screen_height:
            self.rect.y = 0
    
    def draw_background(self):
        """Draw the background image to the screen."""
        for i in range(2):
            self.screen.blit(self.image, (0, self.rect.y - i * self.rect.height))
