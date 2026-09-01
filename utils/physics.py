"""
Physics calculations for projectile motion
Contains all mathematical formulas and numerical methods
"""

import math
from utils.constants import AIR_DENSITY


class PhysicsEngine:
    """Advanced physics calculations for projectile motion"""
    
    @staticmethod
    def calculate_velocity_components(speed, angle):
        """
        Calculate horizontal and vertical velocity components
        
        Parameters:
        speed (float): Initial speed in m/s
        angle (float): Launch angle in degrees
        
        Returns:
        tuple: (vx, vy) velocity components in m/s
        """
        radians = math.radians(angle)
        vx = speed * math.cos(radians)
        vy = speed * math.sin(radians)
        return vx, vy
    
    @staticmethod
    def calculate_air_resistance(vx, vy, drag_coefficient, area, mass):
        """
        Calculate air resistance acceleration components
        Formula: F_drag = 0.5 * ρ * v² * Cd * A
        Acceleration: a = F_drag / m
        
        Parameters:
        vx, vy (float): Velocity components
        drag_coefficient (float): Cd value
        area (float): Cross-sectional area in m²
        mass (float): Mass in kg
        
        Returns:
        tuple: (ax_drag, ay_drag) acceleration components
        """
        speed = math.sqrt(vx ** 2 + vy ** 2)
        if speed == 0:
            return 0, 0
        
        # Drag force magnitude
        drag_force = 0.5 * AIR_DENSITY * speed ** 2 * drag_coefficient * area
        
        # Calculate deceleration (a = F/m)
        drag_acceleration = drag_force / mass
        
        # Calculate components (opposite to velocity direction)
        ax_drag = -drag_acceleration * (vx / speed)
        ay_drag = -drag_acceleration * (vy / speed)
        
        return ax_drag, ay_drag
    
    @staticmethod
    def predict_trajectory(x0, y0, vx, vy, gravity, mass=1.0, 
                          drag_coefficient=0, area=0, time_step=0.05, max_time=10):
        """
        Predict future trajectory points using numerical integration
        
        Parameters:
        x0, y0 (float): Initial position
        vx, vy (float): Initial velocity components
        gravity (float): Gravitational acceleration
        mass (float): Mass for drag calculations
        drag_coefficient (float): Drag coefficient
        area (float): Cross-sectional area
        time_step (float): Integration time step
        max_time (float): Maximum prediction time
        
        Returns:
        list: List of (x, y) trajectory points
        """
        points = []
        x, y = x0, y0
        current_vx, current_vy = vx, vy
        
        for _ in range(int(max_time / time_step)):
            if y < 0:
                break
            
            points.append((x, y))
            
            # Apply gravity
            current_vy -= gravity * time_step
            
            # Apply air resistance if enabled
            if drag_coefficient > 0:
                ax_drag, ay_drag = PhysicsEngine.calculate_air_resistance(
                    current_vx, current_vy, drag_coefficient, area, mass
                )
                current_vx += ax_drag * time_step
                current_vy += ay_drag * time_step
            
            # Update position
            x += current_vx * time_step
            y += current_vy * time_step
        
        return points
    
    @staticmethod
    def calculate_range(initial_x, initial_y, vx, vy, gravity, 
                        drag_coefficient=0, area=0, mass=1.0, accuracy=0.01):
        # Calculate total range using numerical integration and returns total horizontal distance traveled as a float
        x = initial_x
        y = initial_y
        current_vx, current_vy = vx, vy
        
        while y >= 0:
            x += current_vx * accuracy
            y += current_vy * accuracy
            
            current_vy -= gravity * accuracy
            
            if drag_coefficient > 0:
                ax_drag, ay_drag = PhysicsEngine.calculate_air_resistance(
                    current_vx, current_vy, drag_coefficient, area, mass
                )
                current_vx += ax_drag * accuracy
                current_vy += ay_drag * accuracy
        
        return x - initial_x
    
    @staticmethod
    def calculate_max_height(initial_y, vy, gravity):
        """
        Calculate maximum height using v² = u² + 2as
        At max height, final vertical velocity = 0
        """
        if vy <= 0:
            return initial_y
        
        max_height = initial_y + (vy ** 2) / (2 * gravity)
        return max_height
    
    @staticmethod
    def calculate_time_of_flight(initial_y, vy, gravity):
        """
        Calculate total time of flight (effectively this is just the quadratic formula)
        """
        if gravity == 0:
            return float('inf')
        
        a = -0.5 * gravity
        b = vy
        c = initial_y
        
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return 0
        
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        
        # Return positive time
        if t1 > 0:
            return t1
        return t2 if t2 > 0 else 0