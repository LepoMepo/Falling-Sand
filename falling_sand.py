import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
GRID_SIZE = 10

running = True


class Grid:
    def __init__(self, width, height):
        self.rows = width // GRID_SIZE
        self.columns = height // GRID_SIZE

        self.current_grid = [[0 for _ in range(self.columns)] for __ in range(self.rows)]
        self.previous_grid = [[0 for _ in range(self.columns)] for __ in range(self.rows)]

    def add_sand(self, x, y):
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            self.current_grid[x // GRID_SIZE][y // GRID_SIZE] = 1

    def update_grid(self):
        self.previous_grid = self.current_grid
        self.current_grid = [[0 for _ in range(self.columns)] for __ in range(self.rows)]
        for i in range(self.rows - 1, -1, -1):
            if 0 <= i <= (SCREEN_WIDTH // GRID_SIZE) - 1:
                for j in range(self.columns - 1, -1, -1):
                    if 0 <= j < (SCREEN_HEIGHT // GRID_SIZE):
                        if self.previous_grid[i][j]:
                            # Check boundary cells
                            if j == (SCREEN_HEIGHT // GRID_SIZE) - 1:
                                self.current_grid[i][j] = 1
                            elif i == 0:
                                if not self.previous_grid[i + 1][j + 1]:
                                    self.current_grid[i + 1][j + 1] = 1
                                else:
                                    self.current_grid[i][j] = 1
                            elif i == (SCREEN_WIDTH // GRID_SIZE) - 1:
                                if not self.previous_grid[i - 1][j + 1]:
                                    self.current_grid[i - 1][j + 1] = 1
                                else:
                                    self.current_grid[i][j] = 1
                            # Check if bottom cell is empty
                            elif not self.previous_grid[i][j + 1]:
                                self.current_grid[i][j + 1] = 1
                            # Check if left side or right side bottom cell is empty
                            else:
                                if (self.previous_grid[i][j + 1] and not self.previous_grid[i + 1][j + 1] and
                                        not self.previous_grid[i - 1][j + 1]):
                                    self.current_grid[i + random.choice([-1, 1])][j] = 1
                                elif not self.previous_grid[i - 1][j + 1]:
                                    self.current_grid[i - 1][j + 1] = 1
                                elif not self.previous_grid[i + 1][j + 1]:
                                    self.current_grid[i + 1][j + 1] = 1
                                else:
                                    self.current_grid[i][j] = 1
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.current_grid[i][j]:
                    pygame.draw.rect(screen, SAND_COLOR,
                                     (int(i * GRID_SIZE), int(j * GRID_SIZE), GRID_SIZE * 2, GRID_SIZE * 2))


grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    left_button = pygame.mouse.get_pressed()[0]
    if left_button:
        x, y = pygame.mouse.get_pos()
        grid.add_sand(x, y)
        grid.draw_grid()

    grid.update_grid()

    clock.tick(50)
    pygame.display.flip()

pygame.quit()
