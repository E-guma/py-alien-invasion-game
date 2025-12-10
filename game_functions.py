"""A module for miscellaneous functions for alien_invasion.py"""
import sys
from os import path
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, settings, screen, stats, sb, ship, aliens, bullets):
        """Respond to Keydown events"""
        if event.key == pygame.K_RIGHT:
            # Set right movement True
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Set left movement True
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if stats.game_active:
                # Fire new bullets on screeen
                fire_bullet(settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            close_game(stats)            
        elif event.key == pygame.K_p:
            if not stats.game_active:
              start_game(settings, screen, stats, sb, ship, aliens, bullets)            
                
def fire_bullet(settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)
                    
def check_keyup_events(event, ship):
        """"Respond to Keyup events"""
        if event.key == pygame.K_RIGHT:
            # Set right movement False
            ship.moving_right = False        
        elif event.key == pygame.K_LEFT:
            # Set left movement False
            ship.moving_left = False        
                
def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypress and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship) 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, event)
            
def close_game(stats):
    """Close the game and save high score."""
    save_high_score(stats)
    pygame.quit()
    sys.exit()
            
def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, event):
    """Start a new game when the player clicks Play."""
    if play_button.rect.collidepoint(event.pos) and not stats.game_active:
        start_game(settings, screen, stats, sb, ship, aliens, bullets)
                
def start_game(settings, screen, stats, sb, ship, aliens, bullets):
    """Restart Game play"""
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics and settings
    stats.reset_stats()
    stats.game_active = True
    settings.initialize_dynamic_settings()
    # Reset the scoreboard elements.
    sb.prep_images()
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    # Create a new fleet and center the ship.
    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()
        
            
def update_screen(screen, settings, stats, sb, bg, ship, aliens, bullets, play_button):
    """Updates screen elements on each loop"""
    # Fill the screen with background color.
    bg.draw_background()
    # Draw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Draw ship to screen
    ship.blitme()    
    # Draw alien to screen
    aliens.draw(screen)
    # Draw the score information
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Check for collisions
    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)      

def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Update the score if aliens are hit
    if collisions:
        update_score(settings, stats, sb, collisions)    

    if len(aliens) == 0:
        start_new_level(settings, screen, stats, sb, ship, aliens, bullets)  
        
def update_score(settings, stats, sb, collisions):
    """Updates Score or High score when hit aliens"""
    for aliens_hit in collisions.values():
        stats.score += settings.alien_points * len(aliens_hit)
        sb.prep_score()
    check_high_score(stats, sb)
    
def start_new_level(settings, screen, stats, sb, ship, aliens, bullets):
    """Destroy existing bullets, speed up game, create new fleet, and level up"""
    bullets.empty()
    settings.increase_speed()
    create_fleet(settings, screen, ship, aliens)
    stats.level += 1
    sb.prep_level()

def get_number_aliens_x(settings, alien_width):
    """Determine the number of aliens that fit in a row."""    
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien_height = alien.rect.height
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)

    
def create_fleet(settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break
    
def change_fleet_direction(settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def ship_hit(settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        aliens.empty()

def check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
            break

def update_aliens(settings, stats, sb, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, sb, screen, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(settings, stats, sb, screen, ship, aliens, bullets)
        
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()        
        
def high_score_path():
    """Get the file path for the high score file."""
    return path.join(path.dirname(__file__), 'high_score.txt')

def save_high_score(stats):
    """Save the high score to a file."""
    with open(high_score_path(), 'w') as f:
        f.write(str(stats.high_score))       
        
        