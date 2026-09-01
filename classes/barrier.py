"""
Barrier class - Handles obstacle placement and collision detection
"""

import pygame
import utils.constants as constants


class Barrier:
    # Obstacle that blocks projectiles
    
    def __init__(self, x, y, width, height):
        # x, y (float): Position of bottom-left corner in meters
        self.x = x
        self.y = y
        # width, height (float): Dimensions in meters
        self.width = width
        self.height = height
    
    def draw(self, screen, scale):
        #Draw barrier
        rect = pygame.Rect(
            int(self.x * scale),
            constants.HEIGHT - constants.GROUND_HEIGHT - int((self.y + self.height) * scale),
            int(self.width * scale),
            int(self.height * scale)
        )
        
        # Draw 2D effect
        pygame.draw.rect(screen, constants.BROWN, rect)
        pygame.draw.rect(screen, constants.BLACK, rect, 2)
        
        # Add texture lines
        for i in range(3):
            line_y = rect.y + rect.height * (i + 1) // 4
            pygame.draw.line(screen, (100, 50, 0), 
                           (rect.x, line_y), 
                           (rect.x + rect.width, line_y), 1)
    
    def check_collision(self, projectile):
        # Check if projectile collides with barrier and returns True if collision detected
        if not projectile.active:
            return False
        
        px = projectile.x
        py = projectile.y
        
        if (self.x <= px <= self.x + self.width and 
            self.y <= py <= self.y + self.height):
            projectile.active = False
            return True
        
        return False