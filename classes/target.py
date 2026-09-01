"""
Target class - Handles target positioning, collision detection, and drawing
"""

import pygame
import math
import utils.constants as constants


class Target:
    #Target for projectile to hit
    
    def __init__(self, x, y, radius):
        # x, y (float): Position in meters
        self.x = x
        self.y = y
        # radius (int): Radius in pixels
        self.radius = radius
        self.hit = False
        # scale
    
    def draw(self, screen, scale):
        # Draw target
        screen_x = int(self.x * scale)
        screen_y = constants.HEIGHT - constants.GROUND_HEIGHT - int(self.y * scale)
        
        color = constants.GREEN if self.hit else constants.ORANGE
        
        # Draw outer ring
        pygame.draw.circle(screen, color, (screen_x, screen_y), self.radius, 3)
        
        # Draw inner circle
        pygame.draw.circle(screen, color, (screen_x, screen_y), self.radius - 5, 2)
        
        # Draw center dot
        pygame.draw.circle(screen, color, (screen_x, screen_y), 3)
        
        # Draw crosshair
        pygame.draw.line(screen, color, 
                        (screen_x - self.radius, screen_y),
                        (screen_x + self.radius, screen_y), 2)
        pygame.draw.line(screen, color,
                        (screen_x, screen_y - self.radius),
                        (screen_x, screen_y + self.radius), 2)
        
        # Show coordinates if not hit
        if not self.hit:
            font = pygame.font.SysFont("Arial", 12)
            coord_text = font.render(f"({round(self.x,2)}m, {round(self.y,2)}m)", True, constants.BLACK)
            screen.blit(coord_text, (screen_x - 20, screen_y - self.radius - 15))
    
    def check_collision(self, projectile, scale):
        # Check if projectile has hit the target anf returns True if collision detected
        dx = self.x - projectile.x
        dy = self.y - projectile.y
        
        # Convert radius to meters (approximate)
        target_radius_m = self.radius / scale
        projectile_radius_m = projectile.radius / scale
        
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance <= target_radius_m + projectile_radius_m:
            self.hit = True
            return True
        
        return False
    
    def reset(self):
        # Reset hit status (good to make method as code reads better)
        self.hit = False