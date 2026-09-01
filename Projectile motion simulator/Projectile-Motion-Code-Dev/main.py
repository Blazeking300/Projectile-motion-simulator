from classes.simulation import Simulation


def main():
    # Print this out in terminal (may remove later, not very useful)
    print("\n" + "="*60)
    print("   ADVANCED PROJECTILE MOTION SIMULATOR")
    print("="*60)
    print("\nInitializing simulation...")
    print("\nControls:")
    print("  ↑/↓          - Change launch angle")
    print("  ←/→          - Change launch speed")
    print("  G/H          - Adjust gravity")
    print("  M/N          - Adjust mass")
    print("  Z            - Toggle air resistance")
    print("  X/C          - Adjust drag coefficient")
    print("  SPACE        - Launch projectile")
    print("  R            - Reset")
    print("  Left Mouse   - New target location")
    print("  W/A/S/D      - Move launcher")
    print("  -/+/V/E/P/I  - Toggle visual elements")
    print("  ENTER        - Pause")
    print("  1/2/3/4      - Gravity presets")
    print("\nStarting simulator...\n")
    
    # Create and run simulation
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()