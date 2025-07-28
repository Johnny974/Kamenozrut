import pygame
import random


class Game:
    def __init__(self, grid_start_x, grid_start_y, square_size, offset, grid_height=12, grid_width=20):
        self.grid_start_x = grid_start_x
        self.grid_start_y = grid_start_y
        self.square_size = square_size
        self.offset = offset
        self.grid_height = grid_height
        self.grid_width = grid_width
        # TODO v nastaveniach si vybrať color pallete
        #self.colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]
        self.colors = [(49, 86, 89), (65, 211, 189), (186, 50, 79), (255, 186, 73)]
        self.button_pressed = False
        self.grid = []

    def update_grid(self, new_grid):
        self.grid = new_grid
        return self.grid

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        for row in self.grid:
            for column in row:
                if column is not None:
                    pygame.draw.rect(screen, column[1], column[0])

    def highlight_connected_squares(self, squares, screen):
        for square in squares:
            if square is not None:
                new_square = pygame.Rect(self.grid[square[0]][square[1]][0].left - 2,
                                         self.grid[square[0]][square[1]][0].top - 2,
                                         self.grid[square[0]][square[1]][0].width + 4,
                                         self.grid[square[0]][square[1]][0].height + 4)
                pygame.draw.rect(screen, (255, 255, 255), new_square)

    def initialize_grid(self):
        for i in range(self.grid_height):
            row = []
            color_row = []
            for j in range(self.grid_width):
                rect = (pygame.Rect(self.grid_start_x + j * self.offset + j * self.square_size,
                                    self.grid_start_y + i * self.offset + i * self.square_size,
                                    self.square_size, self.square_size), random.choice(self.colors))
                row.append(rect)
                color_row.append(rect[1])
            self.grid.append(row)
        return self.grid

    def find_connected_squares(self, start_row, start_col, color):
        to_check = [(start_row, start_col)]
        connected = set()
        connected.add((start_row, start_col))
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while to_check:
            row, col = to_check.pop(0)
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (0 <= new_row < self.grid_height and 0 <= new_col < self.grid_width
                        and self.grid[new_row][new_col] is not None
                        and self.grid[new_row][new_col][1] == color and (new_row, new_col) not in connected):
                    connected.add((new_row, new_col))
                    to_check.append((new_row, new_col))
        return list(connected)

    def drop_squares_in_grid(self, deleted_squares):
        columns = set(col for row, col in deleted_squares)
        #grid_copy = self.grid.copy()
        for col in columns:
            column_values = [self.grid[r][col] for r in range(self.grid_height)]
            num_of_none = column_values.count(None)
            for i in range(num_of_none):
                column_values = remove_last_occurrence(column_values, None)
                column_values.insert(0, None)
            for index, cell in enumerate(column_values):
                if cell is not None:
                    rect, color = cell
                    rect.top = (self.grid_start_y + index * self.offset + index * self.square_size)
            for row in range(self.grid_height):
                self.grid[row][col] = column_values[row]

        for row in self.grid:
            color_row = []
            for cell in row:
                if cell is not None:
                    color_row.append(cell[1])  # vezmeme len farbu
                else:
                    color_row.append(None)
            #print(color_row)


        #self.update_grid(grid_copy)
            # print(self.grid)
                #self.grid[self.grid_height - 1 - j][col] = column_values[j]
        # for square in deleted_squares:
        #     print(f'Štvorec: {square}')
        #     for i in range(0, square[0]):
        #         self.grid[square[0] - i][square[1]] = self.grid[square[0] - i - 1][square[1]]
        #         print(f'Štvorec z radu: {self.grid[square[0]-i][square[1]]}')
        #     if self.grid[0][square[1]] is not None:
        #         self.grid[0][square[1]] = None

    def handle_move(self, row, col, color):
        if 0 > row >= self.grid_height and 0 > col >= self.grid_width:
            return {"status": "error", "message": "Neplatná pozícia!"}
        if self.grid[row][col] is None:
            return {"status": "error", "message": "Políčko je prázdne!"}

        connected_squares = self.find_connected_squares(row, col, color)
        if len(connected_squares) > 1:
            for square in connected_squares:
                self.grid[square[0]][square[1]] = None

        self.drop_squares_in_grid(connected_squares)
        return self.grid


def remove_last_occurrence(lst, value):
    rev = lst[::-1]
    rev.remove(value)
    return rev[::-1]