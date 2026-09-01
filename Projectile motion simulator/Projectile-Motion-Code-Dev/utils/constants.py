"""
Constants for the Projectile Motion Simulator
All units are in SI (meters, seconds, kg)
"""

# Display settings
WIDTH = 1400
HEIGHT = 800
SCALE = 10  # pixels per meter
FPS = 60
GROUND_HEIGHT = 100

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
DARK_GREEN = (34, 139, 34)
BLUE = (50, 150, 255)
DARK_BLUE = (25, 25, 112)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

# Physics constants (gravity in m/s²)
EARTH_GRAVITY = 9.81
MOON_GRAVITY = 1.62
MARS_GRAVITY = 3.71
JUPITER_GRAVITY = 24.79

# Default values
DEFAULT_ANGLE = 45
DEFAULT_SPEED = 50
DEFAULT_GRAVITY = EARTH_GRAVITY
DEFAULT_MASS = 1.0

# Air resistance
AIR_DENSITY = 1.225  # kg/m³ at sea level
DEFAULT_DRAG_COEFFICIENT = 0.47  # sphere
DEFAULT_AREA = 0.01  # m² (approximate cross-section)

# Grid settings
GRID_SPACING = 10  # meters
GRID_ALPHA = 50

# Initial launch position (meters)
LAUNCH_X = 5
LAUNCH_Y = 0