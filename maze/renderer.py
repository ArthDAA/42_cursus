# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ccolnat <ccolnat@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 18:55:08 by ccolnat         #+#    #+#               #
#  Updated: 2026/06/25 18:55:09 by ccolnat         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
import os
from mazegen.generator import MazeGenerator

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

COLORS = {
    "WHITE": "\033[37m",
    "CYAN": "\033[36m",
    "GREEN": "\033[32m",
    "RED": "\033[31m",
    "YELLOW": "\033[33m",
    "MAGENTA": "\033[35m"
}

COLORS_INVERSE = {val: key for key, val in COLORS.items()}

RESET = "\033[0m"
FULL = "\u2588\u2588"

EMPTY = "  "
PATH = "\u2591\u2591"


class MazeRenderer:
    """Renders a maze in the terminal using ASCII and ANSI colors.

    Attributes:
        maze: The MazeGenerator instance to render.
        entry: The entry coordinates (x, y).
        exit: The exit coordinates (x, y).
        wall_color: The current wall color.
        solve_path_color: The current solve path color.
        pattern_color: The current pattern color.
        show_path: Whether to show the solution path.
        path: The solution path as a list of directions.
    """

    def __init__(
        self,
        maze: MazeGenerator,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initializes the MazeRenderer.

        Args:
            maze: The MazeGenerator instance to render.
            entry: The entry coordinates (x, y).
            exit: The exit coordinates (x, y).
        """
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.wall_color = COLORS["WHITE"]
        self.solve_path_color = COLORS["CYAN"]
        self.pattern_color = COLORS["YELLOW"]
        self.show_path = False
        self.path: list[str] = []
        self.path_cells: set[tuple[int, int]] = set()

    def get_wall_color(self) -> str:
        """Returns the current wall color."""
        return COLORS_INVERSE[self.wall_color]

    def get_solve_path_color(self) -> str:
        """Returns the current solve path color."""
        return COLORS_INVERSE[self.solve_path_color]

    def get_pattern_color(self) -> str:
        """Returns the current pattern color."""
        return COLORS_INVERSE[self.pattern_color]

    def set_wall_color(self, color_name: str) -> None:
        """Sets the wall color.

        Args:
            color_name: The name of the color to set (e.g., "white", "cyan").
        """
        if color_name.upper() in COLORS:
            self.wall_color = COLORS[color_name.upper()]
        else:
            raise ValueError(f"Invalid color name: {color_name}")

    def set_solve_path_color(self, color_name: str) -> None:
        """Sets the solve path color.

        Args:
            color_name: The name of the color to set (e.g., "white", "cyan").
        """
        if color_name.upper() in COLORS:
            self.solve_path_color = COLORS[color_name.upper()]
        else:
            raise ValueError(f"Invalid color name: {color_name}")

    def set_pattern_color(self, color_name: str) -> None:
        """Sets the pattern color.

        Args:
            color_name: The name of the color to set (e.g., "white", "cyan").
        """
        if color_name.upper() in COLORS:
            self.pattern_color = COLORS[color_name.upper()]
        else:
            raise ValueError(f"Invalid color name: {color_name}")

    def compute_path_cells(self) -> None:
        """Computes the set of cells that belong to the solution path."""
        self.path = self.maze.solve(self.entry, self.exit)
        self.path_cells = set()
        x, y = self.entry
        self.path_cells.add((x, y))
        moves = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        for step in self.path:
            dx, dy = moves[step]
            x, y = x + dx, y + dy
            self.path_cells.add((x, y))

    def get_cell_display(self, x: int, y: int) -> str:
        """Returns the display string for a cell.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.

        Returns:
            A colored string representing the cell.
        """
        if (x, y) == self.entry:
            return COLORS["GREEN"] + FULL + RESET
        if (x, y) == self.exit:
            return COLORS["RED"] + FULL + RESET
        if self.show_path and (x, y) in self.path_cells:
            return self.solve_path_color + FULL + RESET
        if (x, y) in self.maze.pattern_cells:
            return self.pattern_color + PATH + RESET
        return EMPTY

    def render(self) -> None:
        """Renders the maze in the terminal using ASCII and ANSI colors."""
        os.system("clear")
        grid = self.maze.grid
        width = self.maze.width
        height = self.maze.height
        wall = self.wall_color + FULL + RESET
        solve_path_segment_color = self.solve_path_color + FULL + RESET

        self.compute_path_cells()

        for y in range(height):
            line_top = ""
            line_mid = ""

            for x in range(width):
                cell = grid[y][x]

                path_segment_north = (
                    solve_path_segment_color if self.show_path
                    and (x, y) in self.path_cells
                    and (x, y - 1) in self.path_cells else EMPTY)

                line_top += wall
                line_top += wall if cell & NORTH else path_segment_north

                path_segment_west = (
                    solve_path_segment_color if self.show_path
                    and (x, y) in self.path_cells
                    and (x - 1, y) in self.path_cells else EMPTY)

                line_mid += wall if cell & WEST else path_segment_west
                line_mid += self.get_cell_display(x, y)

            line_top += wall
            line_mid += wall

            print(line_top)
            print(line_mid)

        line_bot = ""
        for x in range(width * 2):
            line_bot += wall
        line_bot += wall
        print(line_bot)
