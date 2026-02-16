import pygame
import random
import math

GRID_SIZE = 150       # Size of the "atom" grid
SCALE = 4             # Visual size of each square
WINDOW_SIZE = GRID_SIZE * SCALE
FPS = 60

TEMP = 2.269          # Critical Temp (T)
MAGNETIC_FIELD = 0.0  # External Force (H)

COLOR_NORTH = (255, 50, 50)  # Red
COLOR_SOUTH = (50, 50, 255)  # Blue

def update_ising(grid, temp, field):
    """
    Standard Metropolis Algorithm:
    1. Pick a random pixel.
    2. Calculate energy change (dE) if it were to flip.
    3. Flip it if dE < 0, or with probability e^(-dE/T).
    """
    # For speed in pure Python, we do 'N' random attempts per frame
    # instead of looping through every pixel in order.
    for _ in range(GRID_SIZE * GRID_SIZE):
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        
        spin = grid[r][c]
        
        # Sum of 4 neighbors (Up, Down, Left, Right) with wrap-around
        neighbors = (grid[(r + 1) % GRID_SIZE][c] +
                     grid[(r - 1) % GRID_SIZE][c] +
                     grid[r][(c + 1) % GRID_SIZE] +
                     grid[r][(c - 1) % GRID_SIZE])
        
        # Energy change formula: dE = 2 * spin * (neighbors + field)
        dE = 2 * spin * (neighbors + field)
        
        # This is the metropolis part
        if dE <= 0:
            grid[r][c] *= -1
        elif random.random() < math.exp(-dE / temp):
            grid[r][c] *= -1

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# Create tiny surface and grid
calc_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
grid = [[random.choice([1, -1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

current_temp = TEMP
current_field = MAGNETIC_FIELD

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Input: UP/DOWN for Temp, LEFT/RIGHT for Magnetic Field
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: current_temp += 0.05
    if keys[pygame.K_DOWN]: current_temp = max(0.01, current_temp - 0.05)
    if keys[pygame.K_RIGHT]: current_field += 0.1  # Pull towards Red
    if keys[pygame.K_LEFT]: current_field -= 0.1   # Pull towards Blue
    if keys[pygame.K_SPACE]: current_field = 0     # Reset Field

    update_ising(grid, current_temp, current_field)

    # Drawing Step (Direct Pixel Access)
    px_array = pygame.PixelArray(calc_surface)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            px_array[c, r] = COLOR_NORTH if grid[r][c] == 1 else COLOR_SOUTH
    px_array.close()

    # Scale and Show
    scaled_surf = pygame.transform.scale(calc_surface, (WINDOW_SIZE, WINDOW_SIZE))
    screen.blit(scaled_surf, (0, 0))
    
    pygame.display.flip()
    pygame.display.set_caption(f"Temp: {current_temp:.2f} | Field: {current_field:.1f}")
    clock.tick(FPS)

pygame.quit()