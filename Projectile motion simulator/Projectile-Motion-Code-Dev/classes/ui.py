"""
UI class - Handles all user interface elements and displays
"""

import pygame
import utils.constants as constants


class UI:
    # UI with tabs and detailed information
    
    def __init__(self, simulation):
        pygame.font.init()
        
        self.sim = simulation
        
        # Fonts
        self.font_large = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 20)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_bold = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.panel_width = 340
        self.active_tab = 0  # 0=controls, 1=physics, 2=stats
        self.tab_rects = []
    
    def draw_panel(self, screen):
        # Draw the main info panel
        panel_x = constants.WIDTH - self.panel_width
        
        # Semi-transparent panel
        panel_surface = pygame.Surface((self.panel_width, constants.HEIGHT), pygame.SRCALPHA)
        panel_surface.fill((240, 240, 240, 235))
        screen.blit(panel_surface, (panel_x, 0))
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100), (panel_x, 0, self.panel_width, constants.HEIGHT), 2)
        
        return panel_x
    
    def draw_tabs(self, screen, panel_x):
        # Draw tab buttons
        tab_width = self.panel_width // 3
        tabs = ["Controls", "Physics", "Stats"]
        self.tab_rects = []
        
        for i, tab in enumerate(tabs):
            tab_rect = pygame.Rect(panel_x + i * tab_width, 0, tab_width, 40)
            self.tab_rects.append(tab_rect)
            
            if self.active_tab == i:
                color = (70, 130, 200)
                text_color = constants.WHITE
            else:
                color = (180, 180, 180)
                text_color = constants.BLACK
            
            pygame.draw.rect(screen, color, tab_rect)
            pygame.draw.rect(screen, (100, 100, 100), tab_rect, 1)
            
            text = self.font_medium.render(tab, True, text_color)
            text_rect = text.get_rect(center=tab_rect.center)
            screen.blit(text, text_rect)
        
        return panel_x + 10, 50
    
    def draw_controls(self, screen, x, y):
        # Draw controls information
        controls = [
            ("Physics Controls:", None),
            ("↑/↓", "Angle ±1°"),
            ("←/→", "Speed ±2 m/s"),
            ("G/H", "Gravity ±0.5 m/s²"),
            ("M/N", "Mass ±0.1 kg"),
            ("Z", "Toggle Air Resistance"),
            ("X/C", "Drag Coefficient ±0.01"),
            ("", ""),
            ("Visual Controls:", None),
            ("-", "Zoom Out"),
            ("+", "Zoom IN"),
            ("V", "Toggle Vectors"),
            ("E", "Toggle Energy Bars"),
            ("P", "Toggle Prediction"),
            ("I", "Toggle Grid"),
            ("", ""),
            ("Actions:", None),
            ("SPACE", "Launch Projectile"),
            ("R", "Reset"),
            ("Left Mouse", "New Target Location"),
            ("ENTER", "Pause Simulation"),
            ("1/2/3/4", "Gravity Presets"),
            ("W/A/S/D", "Move Launcher"),
            ("", ""),
            ("Gravity Presets:", None),
            ("1", "Earth (9.81 m/s²)"),
            ("2", "Moon (1.62 m/s²)"),
            ("3", "Mars (3.71 m/s²)"),
            ("4", "Jupiter (24.79 m/s²)"),
        ]
        
        current_y = y
        for key, desc in controls:
            if key == "" and desc == "":
                current_y += 10
                continue
            
            if desc is None:  # Section header
                text = self.font_bold.render(key, True, (0, 0, 139))
                screen.blit(text, (x, current_y))
                current_y += 30
            else:
                key_text = self.font_small.render(key, True, constants.BLACK)
                desc_text = self.font_small.render(desc, True, (80, 80, 80))
                screen.blit(key_text, (x, current_y))
                screen.blit(desc_text, (x + 80, current_y))
                current_y += 25
    
    def draw_physics_info(self, screen, x, y):
        # Draw current physics parameters
        params = [
            ("Current Parameters:", None),
            ("", ""),
            (f"Launch Angle: {self.sim.angle}°", None),
            (f"Launch Speed: {self.sim.speed} m/s", None),
            (f"Gravity: {self.sim.gravity:.2f} m/s²", None),
            (f"Mass: {self.sim.mass:.2f} kg", None),
            ("", ""),
            (f"Air Resistance: {'ON' if self.sim.use_air_resistance else 'OFF'}", None),
        ]
        
        if self.sim.use_air_resistance:
            params.append((f"Drag Coefficient: {self.sim.drag_coefficient:.2f}", None))
            params.append((f"Cross-section Area: 0.01 m²", None))
        
        params.extend([
            ("", ""),
            ("Useful Formulas:", None),
            ("", ""),
            ("Range (no drag):", None),
            ("R = v²·sin(2θ)/g", None),
            ("", ""),
            ("Max Height:", None),
            ("H = v²·sin²(θ)/(2g)", None),
            ("", ""),
            ("Time of Flight:", None),
            ("T = 2v·sin(θ)/g", None),
        ])
        
        current_y = y
        for text, _ in params:
            if text == "":
                current_y += 8
                continue
                
            if text == "Current Parameters:" or text == "Useful Formulas:":
                render = self.font_bold.render(text, True, (0, 0, 139))
            else:
                render = self.font_small.render(text, True, constants.BLACK)
            
            screen.blit(render, (x, current_y))
            current_y += 25
    
    def draw_statistics(self, screen, x, y):
        # Draw statistics
        stats = [
            ("Session Statistics:", None),
            ("", ""),
            (f"Total Shots: {self.sim.shots_fired}", None),
        ]
        
        stats.append((f"Max Range Record: {self.sim.max_range_record:.1f} m", None))
        stats.append(("", ""))
        stats.append(("Current Projectile Data:", None))
        stats.append(("", ""))
        
        if self.sim.projectile:
            proj = self.sim.projectile
            stats.extend([
                (f"Range: {proj.get_range()} m", None),
                (f"Height: {proj.get_height()} m", None),
                (f"Velocity: {proj.get_speed()} m/s", None),
                (f"Time: {proj.time:.2f} s", None),
                (f"Max Height: {proj.max_height:.1f} m", None),
                ("", ""),
                (f"Kinetic Energy: {proj.get_kinetic_energy():.1f} J", None),
                (f"Potential Energy: {proj.get_potential_energy():.1f} J", None),
                (f"Total Energy: {proj.total_energy:.1f} J", None),
            ])
        else:
            stats.append(("No projectile active", None))
            stats.append(("Press SPACE to launch", None))
        
        current_y = y
        for text, _ in stats:
            if text == "":
                current_y += 8
                continue
                
            if text == "Session Statistics:" or text == "Current Projectile Data:":
                render = self.font_bold.render(text, True, (0, 0, 139))
            else:
                render = self.font_small.render(text, True, constants.BLACK)
            
            screen.blit(render, (x, current_y))
            current_y += 25
    
    def handle_click(self, pos):
        # Handle tab clicks
        for i, rect in enumerate(self.tab_rects):
            if rect.collidepoint(pos):
                self.active_tab = i
                return True
        return False
    
    def draw(self, screen):
        # Draw complete UI
        # Handle tab clicks
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.handle_click(mouse_pos)
        
        # Draw panel
        panel_x = self.draw_panel(screen)
        x, y = self.draw_tabs(screen, panel_x)
        
        # Draw active tab content
        if self.active_tab == 0:
            self.draw_controls(screen, x, y)
        elif self.active_tab == 1:
            self.draw_physics_info(screen, x, y)
        elif self.active_tab == 2:
            self.draw_statistics(screen, x, y)
        
        # Draw status indicators
        self.draw_status_indicators(screen)
    
    def draw_status_indicators(self, screen):
        # Draw status indicators at top of panel
        panel_x = constants.WIDTH - self.panel_width
        
        # Paused indicator
        if self.sim.paused:
            paused_text = self.font_medium.render("PAUSED", True, constants.RED)
            screen.blit(paused_text, (panel_x + 10, 775))
        
        # Air resistance indicator
        if self.sim.use_air_resistance:
            drag_text = self.font_small.render("Air Resistance: ACTIVE", True, constants.BLUE)
            screen.blit(drag_text, (panel_x + 10, 750))