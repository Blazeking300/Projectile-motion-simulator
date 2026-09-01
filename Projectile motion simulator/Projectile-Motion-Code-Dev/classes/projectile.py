"""
Projectile class - Handles projectile physics, drawing, and state
"""

import pygame
import math
import utils.constants as constants
from utils.physics import PhysicsEngine


class Projectile:
    # Enhanced projectile with full physics simulation
    
    def __init__(self, x, y, speed, angle, gravity, mass=1.0, 
                 drag_coefficient=0, area=0.01, use_air_resistance=False, vector_toggle=True, energy_toggle=True):
        
        # Position (meters)
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        
        # Motion parameters
        self.speed = speed
        self.angle = angle
        self.vx, self.vy = PhysicsEngine.calculate_velocity_components(speed, angle)
        
        # Physics parameters
        self.gravity = gravity
        self.mass = mass
        self.drag_coefficient = drag_coefficient if use_air_resistance else 0
        self.area = area
        self.use_air_resistance = use_air_resistance
        
        # Visual properties
        self.radius = 8
        self.color = constants.RED
        self.trail_color = constants.BLUE
        # Toggles for vectors and energy bars
        self.vector_toggle = vector_toggle
        self.energy_toggle = energy_toggle
        
        # State tracking
        self.active = True
        self.path = []
        #self.max_trail_length = 500 #can be used to decrease amount of data if it is unable to cope
        
        # Physics data
        self.max_height = y
        self.time = 0
        self.kinetic_energy = 0
        self.potential_energy = 0
        self.total_energy = 0
        
        # Impact data
        self.impact_x = None
        self.impact_speed = None
        
        self.update_energies()
    
    def update_energies(self):
        #Calculate kinetic and potential energy
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        self.kinetic_energy = 0.5 * self.mass * speed ** 2
        self.potential_energy = self.mass * self.gravity * self.y
        self.total_energy = self.kinetic_energy + self.potential_energy
    
    def update(self, dt):
        # Update projectile state with physics from the physics engine
        if not self.active:
            return
        
        self.time += dt
        
        # Apply gravity
        self.vy -= self.gravity * dt
        
        # Apply air resistance
        if self.use_air_resistance and self.drag_coefficient > 0:
            ax_drag, ay_drag = PhysicsEngine.calculate_air_resistance(
                self.vx, self.vy, self.drag_coefficient, self.area, self.mass
            )
            self.vx += ax_drag * dt
            self.vy += ay_drag * dt
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Update energy
        self.update_energies()
        
        # Track max height
        if self.y > self.max_height:
            self.max_height = self.y
        
        # Add to trajectory path
        self.path.append((self.x, self.y))
        #if len(self.path) > self.max_trail_length:  #can be used to decrease amount of data if it is unable to cope
        #    self.path.pop(0)
        
        # Check ground collision
        if self.y <= 0:
            self.y = 0
            self.active = False
            self.impact_speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            self.impact_x = self.x
    
    def draw(self, screen, scale):
        # Draw projectile and trajectory
        screen_x = int(self.x * scale)
        screen_y = constants.HEIGHT - constants.GROUND_HEIGHT - int(self.y * scale)
        
        # Draw trajectory trail
        if len(self.path) > 1:
            converted = []
            for px, py in self.path:
                converted.append((
                    int(px * scale),
                    constants.HEIGHT - constants.GROUND_HEIGHT - int(py * scale)
                ))
            
            # Draw trail with varying thickness
            for i in range(len(converted) - 1):
                thickness = max(1, int(3 * (i / len(converted))))
                pygame.draw.line(screen, self.trail_color, 
                               converted[i], converted[i + 1], thickness)
        
        # Draw glow effect
        for radius_offset in range(self.radius + 4, self.radius, -2):
            glow_color = (255, 50 + radius_offset, 50, 100)
            glow_surface = pygame.Surface((radius_offset * 2, radius_offset * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, 
                             (radius_offset, radius_offset), radius_offset)
            screen.blit(glow_surface, 
                       (screen_x - radius_offset, screen_y - radius_offset))
        
        # Draw main projectile
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        pygame.draw.circle(screen, constants.WHITE, (screen_x, screen_y), self.radius - 2)
        
        # Draw velocity vectors
        self.draw_vectors(screen, screen_x, screen_y, self.vector_toggle)
        
        # Draw energy indicator
        self.draw_energy_indicator(screen, screen_x, screen_y, self.energy_toggle)
    
    def draw_vectors(self, screen, sx, sy, toggle):
        # Draw velocity component vectors
        # Only draws when toggled
        if toggle == True:
            vector_scale = 3
            
            # Horizontal velocity vector (Vx)
            vx_end = (sx + int(self.vx * vector_scale), sy)
            pygame.draw.line(screen, constants.GREEN, (sx, sy), vx_end, 3)
            
            # Vertical velocity vector (Vy)
            vy_end = (sx, sy - int(self.vy * vector_scale))
            pygame.draw.line(screen, constants.YELLOW, (sx, sy), vy_end, 3)
            
            # Resultant velocity vector (Total V)
            v_total_end = (sx + int(self.vx * vector_scale), 
                        sy - int(self.vy * vector_scale))
            pygame.draw.line(screen, constants.ORANGE, (sx, sy), v_total_end, 4)
            
            # Add vector labels
            font = pygame.font.SysFont("Arial", 14)
            vx_text = font.render(f"Vx={round(self.vx, 1)}", True, constants.GREEN)
            vy_text = font.render(f"Vy={round(self.vy, 1)}", True, constants.YELLOW)
            v_text = font.render(f"V={round(self.get_speed(), 1)}", True, constants.ORANGE)
            
            screen.blit(vx_text, (vx_end[0] + 5, vx_end[1] - 10))
            screen.blit(vy_text, (vy_end[0] + 5, vy_end[1] - 20))
            screen.blit(v_text, (v_total_end[0] + 5, v_total_end[1] - 15))
    
    def draw_energy_indicator(self, screen, sx, sy, toggle):
        # Draw visual representation of energy
        # Only draws when toggled
        if toggle == True:
            radius_offset = self.radius + 5
            baseline = sy + radius_offset  # fixed bottom of the bar
            
            # Kinetic energy bar (green)
            ke_height = min(200, int(self.kinetic_energy / 5))
            if ke_height > 0:
                pygame.draw.rect(screen, constants.GREEN,
                                (sx - radius_offset - 5, baseline - ke_height,
                                4, ke_height))
            
            # Potential energy bar (red)
            pe_height = min(200, int(self.potential_energy / 5))
            if pe_height > 0:
                pygame.draw.rect(screen, constants.RED,
                                (sx - radius_offset, baseline - pe_height,
                                4, pe_height))
        
    def get_range(self):
        # Get current horizontal distance traveled
        return round(self.x - self.start_x, 2)
    
    def get_height(self):
        # Get current height
        return round(self.y, 2)
    
    def get_speed(self):
        # Get current speed
        return round(math.sqrt(self.vx ** 2 + self.vy ** 2), 2)
    
    def get_kinetic_energy(self):
        # Get current kinetic energy
        return round(self.kinetic_energy, 2)
    
    def get_potential_energy(self):
        # Get current potential energy
        return round(self.potential_energy, 2)