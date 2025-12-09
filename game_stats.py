"""Tracking data and statistics for Alien Invasion"""
from game_functions import high_score_path


class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # load High Score from file, and Track High Score
        try:
            with open(high_score_path(), 'r') as f:
                self.high_score = int(f.read())
        except FileNotFoundError:
            self.high_score = 0
                
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1