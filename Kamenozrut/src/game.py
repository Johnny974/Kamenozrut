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
        self.colors = ""
        self.button_pressed = False
        self.grid = []

    def update_grid(self, new_grid):
        self.grid = new_grid
        return self.grid

    def draw(self, screen):
        for row in self.grid:
            for column in row:
                if column is not None:
                    pygame.draw.rect(screen, column[1], column[0])

    def draw_color_scheme_selection(self, screen, colors):
        for row in colors:
            for color in row:
                pygame.draw.rect(screen, color[1], color[0])

    def initialize_grid(self):
        for i in range(self.grid_height):
            row = []
            for j in range(self.grid_width):
                rect = (pygame.Rect(self.grid_start_x + j * self.offset + j * self.square_size,
                                    self.grid_start_y + i * self.offset + i * self.square_size,
                                    self.square_size, self.square_size), random.choice(self.colors))
                row.append(rect)
            self.grid.append(row)
        return self.grid

    # TODO error maybe in this json format of grid
    def serialize_grid(self):
        serialized_grid = [[({"x": rect.x, "y": rect.y}, list(color)) for rect, color in row] for row in self.grid]
        return serialized_grid

    def deserialize_grid(self, data):
        deserialized_grid = [[(pygame.Rect(r["x"], r["y"], self.grid_width, self.grid_height), tuple(color)) for r, color in row] for row
                             in data]
        return deserialized_grid

    def initialize_color_scheme_squares(self, colors):
        color_scheme_grid = []
        x = 690
        y = 580
        for i in range(len(colors)):
            row = []
            for j in range(len(colors[0])):
                rect = (pygame.Rect(x + j * self.offset + j * self.square_size,
                                    y + self.offset + self.square_size,
                                    self.square_size, self.square_size), colors[i][j])
                row.append(rect)
            x += 380
            if i == 1:
                x = 690
                y += 130
            color_scheme_grid.append(row)
        return color_scheme_grid

    def swap_color_palette(self, old_palette, new_palette):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j] is not None:
                    rect, color = self.grid[i][j]
                    index = old_palette.index(color)
                    self.grid[i][j] = (rect, new_palette[index])

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

    def highlight_connected_squares(self, squares, screen):
        for square in squares:
            if square is not None:
                new_square = pygame.Rect(self.grid[square[0]][square[1]][0].left - 2,
                                         self.grid[square[0]][square[1]][0].top - 2,
                                         self.grid[square[0]][square[1]][0].width + 4,
                                         self.grid[square[0]][square[1]][0].height + 4)
                pygame.draw.rect(screen, (255, 255, 255), new_square)

    def handle_move(self, row, col, color):
        # if 0 > row >= self.grid_height and 0 > col >= self.grid_width:
        #     return {"status": "error", "message": "Neplatná pozícia!"}
        # if self.grid[row][col] is None:
        #     return {"status": "error", "message": "Políčko je prázdne!"}

        connected_squares = self.find_connected_squares(row, col, color)
        if len(connected_squares) > 1:
            for square in connected_squares:
                self.grid[square[0]][square[1]] = None
            self.drop_squares_in_grid(connected_squares)
            return len(connected_squares)
        else:
            return 0

    def drop_squares_in_grid(self, deleted_squares):
        columns = set(col for row, col in deleted_squares)
        for col in columns:
            column_values = [self.grid[r][col] for r in range(self.grid_height)]
            num_of_none = column_values.count(None)
            for i in range(num_of_none):
                column_values = remove_last_occurrence(column_values, None)
                column_values.insert(0, None)
            for index, cell in enumerate(column_values):
                if cell is not None:
                    rect, color = cell
                    rect.top = self.grid_start_y + index * self.offset + index * self.square_size
            for row in range(self.grid_height):
                self.grid[row][col] = column_values[row]
        self.shift_columns_left()

    def shift_columns_left(self):
        col = 0
        while col < self.grid_width:
            is_empty = all(self.grid[row][col] is None for row in range(self.grid_height))
            is_empty_last_column = all(self.grid[row][self.grid_width - 1] is None for row in range(self.grid_height))
            if is_empty:
                for j in range(col, self.grid_width - 1):
                    for i in range(self.grid_height):
                        self.grid[i][j] = self.grid[i][j + 1]
                        if self.grid[i][j] is not None:
                            self.grid[i][j][0].left -= self.offset + self.square_size
                if not is_empty_last_column:
                    for k in range(self.grid_height):
                        self.grid[k][self.grid_width - 1] = None
                remaining_cols = [
                    any(self.grid[row][c] is not None for row in range(self.grid_height))
                    for c in range(col, self.grid_width)
                ]
                if not any(remaining_cols):
                    break
            else:
                col += 1

    def is_game_over(self):
        is_grid_empty = all(
            cell is None
            for row in self.grid
            for cell in row
        )
        if is_grid_empty:
            return "You won"

        for row in range(self.grid_height):
            for col in range(self.grid_width):
                cell = self.grid[row][col]
                if cell is None:
                    continue
                _, color = cell

                if col + 1 < self.grid_width:
                    neighbor = self.grid[row][col + 1]
                    if neighbor is not None and neighbor[1] == color:
                        return "There is a possible move"

                # Pozri dole
                if row + 1 < self.grid_height:
                    neighbor = self.grid[row + 1][col]
                    if neighbor is not None and neighbor[1] == color:
                        return "There is a possible move"

        return "No moves left"


def remove_last_occurrence(lst, value):
    rev = lst[::-1]
    rev.remove(value)
    return rev[::-1]


def add_score(num):
    return num * num
