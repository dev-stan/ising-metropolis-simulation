import pygame
import random
import math

GRID_SIZE = 150
SCALE = 4             # Visual size of each square
WINDOW_SIZE = GRID_SIZE * SCALE
FPS = 60

CRITICAL_TEMP = 2.269 
INITIAL_FIELD = 0.0

COLOR_RED = (255, 50, 50)   # Spin +1
COLOR_BLUE = (50, 50, 255)  # Spin -1

def update_ising(grid, temp, field):
    """
    Standard Metropolis Algorithm:
    Iterates through the grid and applies the energy-based flip criteria.
    """
    for _ in range(GRID_SIZE * GRID_SIZE):
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        
        spin = grid[r][c]
        
        # Sum of 4 neighbors with periodic boundary conditions (wrap-around)
        neighbors = (grid[(r + 1) % GRID_SIZE][c] +
                     grid[(r - 1) % GRID_SIZE][c] +
                     grid[r][(c + 1) % GRID_SIZE] +
                     grid[r][(c - 1) % GRID_SIZE])
        
        # Energy change formula: dE = 2 * spin * (neighbors + field)
        dE = 2 * spin * (neighbors + field)
        
        # Metropolis Criterion
        if dE <= 0:
            grid[r][c] *= -1
        elif random.random() < math.exp(-dE / temp):
            grid[r][c] *= -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()

    # Create calculation surface and initial random grid
    calc_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
    grid = [[random.choice([1, -1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    current_temp = CRITICAL_TEMP
    current_field = INITIAL_FIELD
    running = True

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # 2. Controls (Keyboard Input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:    current_temp += 0.05
        if keys[pygame.K_DOWN]:  current_temp = max(0.01, current_temp - 0.05)
        if keys[pygame.K_RIGHT]: current_field += 0.05
        if keys[pygame.K_LEFT]:  current_field -= 0.05
        if keys[pygame.K_SPACE]: current_field = 0.0

        # 3. Physics Update
        update_ising(grid, current_temp, current_field)

        # 4. Rendering Step
        # Using PixelArray for high-speed direct manipulation
        px_array = pygame.PixelArray(calc_surface)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                px_array[c, r] = COLOR_RED if grid[r][c] == 1 else COLOR_BLUE
        px_array.close()

        # Scale the calculation surface to the window size
        scaled_surf = pygame.transform.scale(calc_surface, (WINDOW_SIZE, WINDOW_SIZE))
        screen.blit(scaled_surf, (0, 0))
        
        # UI Updates
        pygame.display.flip()
        pygame.display.set_caption(f"Ising Model | Temp: {current_temp:.2f} | Field: {current_field:.2f}")
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()