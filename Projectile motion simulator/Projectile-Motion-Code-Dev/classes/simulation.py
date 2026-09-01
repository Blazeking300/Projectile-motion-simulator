"""
Simulation class - Main controller for the entire application
"""

import pygame
import math
import utils.constants as constants
from utils.physics import PhysicsEngine
from classes.projectile import Projectile
from classes.target import Target
from classes.barrier import Barrier
from classes.ui import UI


class Simulation:
    # Main simulation controller
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Display setup
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Advanced Projectile Motion Simulator")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Simulation parameters
        self.angle = constants.DEFAULT_ANGLE
        self.speed = constants.DEFAULT_SPEED
        self.gravity = constants.DEFAULT_GRAVITY
        self.mass = constants.DEFAULT_MASS
        self.drag_coefficient = constants.DEFAULT_DRAG_COEFFICIENT
        self.scale = constants.SCALE
        self.use_air_resistance = False
        
        # Visual settings
        self.show_grid = True
        self.show_vectors = True
        self.show_energy = True
        self.show_prediction = True
        
        # trajectories
        self.trajectories = []
        
        # Objects
        self.projectile = None
        self.predictions = []
        
        # Launch point
        self.launch_x = constants.LAUNCH_X
        self.launch_y = constants.LAUNCH_Y
        
        # Create objects
        self.ui = UI(self)
        self.target = Target(70, 10, 15)
        self.barrier = Barrier(40, 0, 6, 25)
        
        # Statistics
        self.shots_fired = 0
        self.hits = 0
        self.max_range_record = 0
    
    def launch_projectile(self):
        # Launch a new projectile
        self.projectile = Projectile(
            self.launch_x, self.launch_y,
            self.speed, self.angle, self.gravity,
            self.mass, self.drag_coefficient, 0.01,
            self.use_air_resistance, self.show_vectors, self.show_energy
        )
        self.shots_fired += 1
    
    def reset(self):
        # Reset current projectile
        self.projectile = None
    
    def move_target(self, mouse_x, mouse_y):
        # Reposition target to clicked position (convert from pixel to simulation units)
        self.target.x = mouse_x / self.scale
        self.target.y = (constants.HEIGHT - constants.GROUND_HEIGHT - mouse_y) / self.scale
        self.target.hit = False
    
    def update_predictions(self):
        # Update trajectory prediction
        if not self.projectile and not self.paused:
            vx, vy = PhysicsEngine.calculate_velocity_components(self.speed, self.angle)
            
            if self.use_air_resistance:
                self.predictions = PhysicsEngine.predict_trajectory(
                    self.launch_x, self.launch_y, vx, vy, self.gravity,
                    self.mass, self.drag_coefficient, 0.01, 0.05, 30
                )
            else:
                self.predictions = PhysicsEngine.predict_trajectory(
                    self.launch_x, self.launch_y, vx, vy, self.gravity,
                    0, 0, 0, 0.05, 30
                )

    def handle_events(self):
        # Handle all input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self.move_target(mouse_x,mouse_y)
            elif event.type == pygame.KEYDOWN:
                # Physics parameters
                if event.key == pygame.K_UP:
                    self.angle += 1
                elif event.key == pygame.K_DOWN:
                    self.angle -= 1
                elif event.key == pygame.K_RIGHT:
                    self.speed += 2
                elif event.key == pygame.K_LEFT:
                    self.speed -= 2
                elif event.key == pygame.K_g:
                    self.gravity += 0.5
                elif event.key == pygame.K_h:
                    self.gravity -= 0.5
                elif event.key == pygame.K_m:
                    self.mass += 0.1
                elif event.key == pygame.K_n:
                    self.mass = max(0.1, self.mass - 0.1)
                
                # moving launcher
                elif event.key == pygame.K_d:
                    self.launch_x += 2
                elif event.key == pygame.K_a:
                    self.launch_x -= 2
                elif event.key == pygame.K_w:
                    self.launch_y += 2
                elif event.key == pygame.K_s:
                    self.launch_y = max(0, self.launch_y - 2)
                
                # Air resistance
                elif event.key == pygame.K_z:
                    self.use_air_resistance = not self.use_air_resistance
                elif event.key == pygame.K_x:
                    self.drag_coefficient = max(0, self.drag_coefficient - 0.01)
                elif event.key == pygame.K_c:
                    self.drag_coefficient += 0.01
                
                # Visual toggles
                elif event.key == pygame.K_v:
                    self.show_vectors = not self.show_vectors
                elif event.key == pygame.K_e:
                    self.show_energy = not self.show_energy
                elif event.key == pygame.K_p:
                    self.show_prediction = not self.show_prediction
                elif event.key == pygame.K_i:
                    self.show_grid = not self.show_grid

                # Zoom controls
                elif event.key == pygame.K_MINUS:
                    self.scale = max(1, self.scale - 1)
                elif event.key == pygame.K_EQUALS:
                    self.scale = min(20, self.scale + 1)

                # Actions
                elif event.key == pygame.K_SPACE:
                    self.launch_projectile()
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_RETURN:
                    self.paused = not self.paused
                
                # Presets
                elif event.key == pygame.K_1:
                    self.gravity = constants.EARTH_GRAVITY
                elif event.key == pygame.K_2:
                    self.gravity = constants.MOON_GRAVITY
                elif event.key == pygame.K_3:
                    self.gravity = constants.MARS_GRAVITY
                elif event.key == pygame.K_4:
                    self.gravity = constants.JUPITER_GRAVITY
        
        # Clamp values
        self.angle = max(1, min(89, self.angle))
        self.speed = max(5, min(150, self.speed))
        self.gravity = max(0.1, min(50, self.gravity))
        self.mass = max(0.1, min(10, self.mass))
    
    def update(self, dt):
        # Update simulation state
        if dt > 0.033:  # Cap delta time
            dt = 0.033
        
        if not self.paused:
            # Update projectile
            if self.projectile:
                self.projectile.update(dt)
                
                if not self.projectile.active and len(self.projectile.path) > 1:
                    if self.projectile.path not in self.trajectories:
                        self.trajectories.append(self.projectile.path)
                
                # Check collisions
                if self.target.check_collision(self.projectile, self.scale):
                    if not self.target.hit:  # First hit
                        self.hits += 1
                
                self.barrier.check_collision(self.projectile)
                
                # Update max range record
                if not self.projectile.active and self.projectile.get_range() > self.max_range_record:
                    self.max_range_record = self.projectile.get_range()
                    
                
            
            # Update predictions
            self.update_predictions()
    
    def draw_grid(self):
        # Draw coordinate grid
        if not self.show_grid:
            return
        
        grid_surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        
        # Draw vertical lines
        for x in range(0, constants.WIDTH, int(constants.GRID_SPACING * self.scale)):
            alpha = constants.GRID_ALPHA if x % (int(constants.GRID_SPACING * self.scale * 5)) == 0 else constants.GRID_ALPHA // 2
            color = (150, 150, 150, alpha)
            pygame.draw.line(grid_surface, color, (x, 0), (x, constants.HEIGHT), 1)
        # Draw horizontal lines
        for y in range(0, constants.HEIGHT - constants.GROUND_HEIGHT, int(constants.GRID_SPACING * self.scale)):
            alpha = constants.GRID_ALPHA if y % (int(constants.GRID_SPACING * self.scale * 5)) == 0 else constants.GRID_ALPHA // 2
            color = (150, 150, 150, alpha)
            pygame.draw.line(grid_surface, color, (0, y), (constants.WIDTH, y), 1)
        self.screen.blit(grid_surface, (0, 0))
    
    def draw_prediction(self):
        # Draw predicted trajectory
        if not self.show_prediction or self.projectile:
            return
        
        if len(self.predictions) > 1:
            converted = []
            for x, y in self.predictions:
                screen_x = int(x * self.scale)
                screen_y = constants.HEIGHT - constants.GROUND_HEIGHT - int(y * self.scale)
                if 0 <= screen_x <= constants.WIDTH and 0 <= screen_y <= constants.HEIGHT:
                    converted.append((screen_x, screen_y))
            
            if len(converted) > 1:
                # Draw dashed line
                for i in range(0, len(converted) - 1, 2):
                    if i + 1 < len(converted):
                        pygame.draw.line(self.screen, (150, 150, 150),
                                       converted[i], converted[i + 1], 2)
                
                # Draw prediction end point
                if len(converted) > 0:
                    pygame.draw.circle(self.screen, (200, 200, 200),
                                     converted[-1], 6, 2)
    
    def draw_background(self):
        # Draw background elements
        # Sky gradient
        sky_height = constants.HEIGHT - constants.GROUND_HEIGHT
        for y in range(sky_height):
            ratio = y / sky_height
            color = (
                int(135 + ratio * 120),
                int(206 + ratio * 49),
                int(235 + ratio * 20)
            )
            pygame.draw.line(self.screen, color, (0, y), (constants.WIDTH, y))
        # Ground
        ground_rect = pygame.Rect(0, constants.HEIGHT - constants.GROUND_HEIGHT, constants.WIDTH, constants.GROUND_HEIGHT)
        pygame.draw.rect(self.screen, constants.DARK_GREEN, ground_rect)
        # Add a darker ground strip at the bottom
        bottom_strip = pygame.Rect(0, constants.HEIGHT - 20, constants.WIDTH, 20)
        pygame.draw.rect(self.screen, (30, 80, 30), bottom_strip)
        # Draw horizontal ground line
        ground_y = constants.HEIGHT - constants.GROUND_HEIGHT
        pygame.draw.line(self.screen, constants.BLACK, (0, ground_y), (constants.WIDTH, ground_y), 2)
    
    def draw_launcher(self):
        # Draw the launch mechanism
        x = int(self.launch_x * self.scale)
        y = constants.HEIGHT - constants.GROUND_HEIGHT - int(self.launch_y * self.scale)
        
        # Draw base platform
        platform_width = 40
        platform_height = 10
        pygame.draw.rect(self.screen, constants.GRAY, 
                (x - platform_width//2, y - platform_height, 
                 platform_width, platform_height))
        
        # Draw launch arm
        angle_rad = math.radians(self.angle)
        arm_length = 25
        arm_end_x = x + arm_length * math.cos(angle_rad)
        arm_end_y = y - arm_length * math.sin(angle_rad)
        arm_end = (int(arm_end_x), int(arm_end_y))
        pygame.draw.line(self.screen, constants.BLACK, (x, y), arm_end, 5)
        
        # Draw launch pad circle
        pygame.draw.circle(self.screen, (150, 150, 150), (x, y), 8)
        pygame.draw.circle(self.screen, constants.BLACK, (x, y), 8, 1)
        
        # Draw angle arc
        arc_radius = 30
        arc_rect = pygame.Rect(x - arc_radius, y - arc_radius, 
                              arc_radius * 2, arc_radius * 2)
        start_angle = math.radians(-90)
        end_angle = math.radians(-90 + self.angle)
        pygame.draw.arc(self.screen, constants.BLUE, arc_rect, start_angle, end_angle, 2)
        
        # Draw angle text
        font = pygame.font.SysFont("Arial", 14)
        angle_text = font.render(f"{self.angle}°", True, constants.BLACK)
        self.screen.blit(angle_text, (x + 15, y - 25))
    
    def draw_colour_reference(self):
        # Draw colour_reference
        colour_reference_items = [
            ("Red", "Projectile"),
            ("Blue", "Trajectory"),
            ("Orange", "Target"),
            ("Brown", "Barrier"),
            ("Green", "Vx Vector"),
            ("Yellow", "Vy Vector"),
            ("Gray Dashed", "Prediction"),
        ]
        
        x = 10
        y = 10
        
        # Draw background
        colour_reference_surface = pygame.Surface((180, 120), pygame.SRCALPHA)
        colour_reference_surface.fill((255, 255, 255, 200))
        pygame.draw.rect(colour_reference_surface, constants.BLACK, (0, 0, 180, 120), 1)
        self.screen.blit(colour_reference_surface, (x, y))
        font = pygame.font.SysFont("Arial", 11)
        for i, (color_name, description) in enumerate(colour_reference_items):
            text = font.render(f"{color_name}: {description}", True, constants.BLACK)
            self.screen.blit(text, (x + 5, y + 5 + i * 14))
    
    def draw_trajectories(self):
        # Draw all previous trajectories
        for path in self.trajectories:
            if len(path) > 1:
                converted = [
                    (int(x * self.scale), constants.HEIGHT - constants.GROUND_HEIGHT - int(y * self.scale))
                    for x, y in path
                ]
                for i in range(len(converted) - 1):
                    pygame.draw.line(self.screen, (0,0,255), converted[i], converted[i + 1], 2)
    
    def draw(self):
        #Draw everything (brings all draw methods together)
        self.draw_background()
        self.draw_grid()
        self.draw_trajectories()
        self.draw_prediction()
        
        self.draw_launcher()
        self.target.draw(self.screen, self.scale)
        self.barrier.draw(self.screen, self.scale)
        
        if self.projectile:
            self.projectile.draw(self.screen, self.scale)
        
        self.ui.draw(self.screen)
        self.draw_colour_reference()
        
        pygame.display.update()
    
    def run(self):
        #Main game loop
        while self.running:
            dt = self.clock.tick(constants.FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            # Update window title with stats
            if self.projectile and self.projectile.active:
                title = f"Range: {self.projectile.get_range():.1f}m | "
                title += f"Height: {self.projectile.get_height():.1f}m | "
                title += f"Speed: {self.projectile.get_speed():.1f}m/s | "
                title += f"Energy: {self.projectile.total_energy:.1f}J"
                pygame.display.set_caption(title)
            else:
                pygame.display.set_caption("Advanced Projectile Motion Simulator")
        
        # Show final statistics
        self.show_statistics()
        pygame.quit()
    
    def show_statistics(self):
        #Display final statistics
        print("\n" + "="*50)
        print("   PROJECTILE MOTION SIMULATOR - FINAL STATISTICS")
        print("="*50)
        print(f"Total Shots Fired: {self.shots_fired}")
        print(f"Maximum Range Record: {self.max_range_record:.1f} meters")
        print("="*50)