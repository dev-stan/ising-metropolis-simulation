import pygame
import random
import math
import asyncio

# --- Configuration ---
GRID_SIZE = 150
SCALE = 4
WINDOW_SIZE = GRID_SIZE * SCALE
FPS = 60

# Physical Constants
CRITICAL_TEMP = 2.269 
MAX_VISUAL_TEMP = 5.0  # For the percentage bar
MAX_VISUAL_FIELD = 2.0 # For the percentage bar

COLOR_RED = (255, 50, 50)
COLOR_BLUE = (50, 50, 255)
COLOR_UI_BG = (0, 0, 0, 150) # Semi-transparent black

def update_ising(grid, temp, field):
    for _ in range(GRID_SIZE * GRID_SIZE):
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        spin = grid[r][c]
        neighbors = (grid[(r + 1) % GRID_SIZE][c] +
                     grid[(r - 1) % GRID_SIZE][c] +
                     grid[r][(c + 1) % GRID_SIZE] +
                     grid[r][(c - 1) % GRID_SIZE])
        dE = 2 * spin * (neighbors + field)
        if dE <= 0 or random.random() < math.exp(-dE / temp):
            grid[r][c] *= -1

async def main():
    # --- Fix for WASM Audio Error ---
    pygame.display.init()
    pygame.font.init()
    # pygame.mixer is NOT initialized here
    
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)

    calc_surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
    grid = [[random.choice([1, -1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    current_temp = CRITICAL_TEMP
    current_field = 0.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # 1. Input Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:    current_temp = min(10.0, current_temp + 0.05)
        if keys[pygame.K_DOWN]:  current_temp = max(0.01, current_temp - 0.05)
        if keys[pygame.K_RIGHT]: current_field = min(2.0, current_field + 0.02)
        if keys[pygame.K_LEFT]:  current_field = max(-2.0, current_field - 0.02)
        if keys[pygame.K_SPACE]: current_field = 0.0

        # 2. Physics Update
        update_ising(grid, current_temp, current_field)

        # 3. Draw Ising Grid
        px_array = pygame.PixelArray(calc_surface)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                px_array[c, r] = COLOR_RED if grid[r][c] == 1 else COLOR_BLUE
        px_array.close()
        
        scaled_surf = pygame.transform.scale(calc_surface, (WINDOW_SIZE, WINDOW_SIZE))
        screen.blit(scaled_surf, (0, 0))

        # 4. Draw UI Overlay
        ui_surf = pygame.Surface((220, 130), pygame.SRCALPHA)
        ui_surf.fill(COLOR_UI_BG)
        
        # Calculate Percentages for Bars
        temp_pct = min(1.0, current_temp / MAX_VISUAL_TEMP)
        # Field bar is centered at 0
        field_pct = (current_field + MAX_VISUAL_FIELD) / (MAX_VISUAL_FIELD * 2)

        # Text Labels
        lines = [
            (f"TEMP: {current_temp:.2f}", (10, 10)),
            (f"FIELD: {current_field:.2f}", (10, 55)),
            ("UP/DN: Temp | L/R: Field", (10, 100)),
            ("SPACE: Reset Field", (10, 115))
        ]
        
        for text, pos in lines:
            txt_img = font.render(text, True, (255, 255, 255))
            ui_surf.blit(txt_img, pos)

        # Draw Progress Bars
        pygame.draw.rect(ui_surf, (100, 100, 100), (10, 35, 200, 10)) # Temp BG
        pygame.draw.rect(ui_surf, (255, 200, 0), (10, 35, 200 * temp_pct, 10)) # Temp Fill
        
        pygame.draw.rect(ui_surf, (100, 100, 100), (10, 80, 200, 10)) # Field BG
        pygame.draw.rect(ui_surf, (0, 255, 255), (10, 80, 200 * field_pct, 10)) # Field Fill

        screen.blit(ui_surf, (10, 10))
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())