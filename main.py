import sys
import pygame
import random
import copy

size = width, height = 650, 650

screen = pygame.display.set_mode(size)
pygame.font.init()

colors = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (238, 225, 201),
    8: (243, 178, 122),
    16: (246, 150, 100),
    32: (247, 124, 95),
    64: (247, 95, 59),
    128: (237, 208, 115),
    256: (237, 201, 80),
    512: (237, 201, 80),
    1024: (237, 201, 80),
    2048: (237, 201, 80),
}

BLACK = (0, 0, 0)
BACKGROUND_COLOR = (187, 173, 160)
FONT = pygame.font.SysFont(None, 36)


class Grid:
    def __init__(self):
        self._grid = [[0, 0, 0, 0] for i in range(4)]

    @staticmethod
    def _join_elements():
        pass

    @property
    def random_free_cell(self):
        zeros_count = 0

        for i in range(4):
            for j in range(4):
                if self._grid[i][j] == 0:
                    zeros_count += 1

        random_index = random.randint(0, zeros_count - 1)
        zeros_count = 0

        for i in range(4):
            for j in range(4):
                if self._grid[i][j] == 0:
                    if random_index == zeros_count:
                        return i, j
                    zeros_count += 1

    def show(self):
        print("=====================")
        for row in self._grid:
            print(f'{" ".join(map(str, row))}')
        print("=====================")

    def fill_random_cell(self):
        row, col = self.random_free_cell
        random_value = 2 if random.randint(1, 4) != 4 else 4
        self._grid[row][col] = random_value
        return self

    def move_left(self):
        changed = False
        for row in self._grid:
            new_row = Grid._join_blocks(row)
            if row != new_row:
                changed = True
                row[:] = new_row[:]

        if changed:
            self.fill_random_cell()
        return self

    def move_right(self):
        changed = False
        for row in self._grid:
            new_row = new_row = Grid._join_blocks(row[::-1])[::-1]
            if row != new_row:
                changed = True
                row[:] = new_row[:]

        if changed:
            self.fill_random_cell()
        return self

    def move_up(self):
        changed = False

        for col in range(4):
            column = [self._grid[i][col] for i in range(4)]
            new_col = Grid._join_blocks(column)

            if new_col != column:
                changed = True
                for i in range(4):
                    self._grid[i][col] = new_col[i]

        if changed:
            self.fill_random_cell()
        return self

    def move_down(self):
        changed = False
        for col in range(4):
            column = [self._grid[i][col] for i in range(4)][::-1]
            new_col = Grid._join_blocks(column)[::-1]

            if new_col != column:
                changed = True
                for i in range(4):
                    self._grid[i][col] = new_col[i]

        if changed:
            self.fill_random_cell()
        return self

    @staticmethod
    def _join_blocks(row):
        count = len(row)

        row = [i for i in row if i]
        new_row = []

        while row:
            if len(row) == 1:
                new_row.append(row[0])
                break

            if row[0] == row[1]:
                row[0] *= 2
                row.pop(1)

            new_row.append(row[0])
            row.pop(0)

        new_row.extend([0 for i in range(4 - len(new_row))])
        return new_row

    @property
    def raw(self):
        return self._grid


def draw_grid(grid: Grid):
    screen.fill(BACKGROUND_COLOR)
    grid_raw = grid.raw
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, colors.get(grid_raw[i][j], BLACK), (10 + 160 * j, 10 + 160 * i, 150, 150))

            if grid_raw[i][j]:
                number = FONT.render(str(grid_raw[i][j]), True, (255, 0, 127))
                screen.blit(number, (70 + 160 * j, 70 + 160 * i))


grid = Grid()
grid.fill_random_cell()
grid.show()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                grid.move_left()
            if event.key == pygame.K_RIGHT:
                grid.move_right()
            if event.key == pygame.K_UP:
                grid.move_up()
            if event.key == pygame.K_DOWN:
                grid.move_down()

            grid.show()

    draw_grid(grid)
    pygame.display.flip()
