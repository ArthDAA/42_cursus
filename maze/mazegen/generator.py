
import random
from typing import Optional, Dict, Tuple
import sys


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

DIRECTIONS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}

PATTERN_42 = [

    (0, 0), (0, 1), (0, 2),
    (1, 2),
    (2, 2), (2, 3), (2, 4),

    (4, 0), (4, 2), (4, 3), (4, 4),
    (5, 0), (5, 2), (5, 4),
    (6, 0), (6, 1), (6, 2), (6, 4),
]

PATTERN_42_WIDTH = 7
PATTERN_42_HEIGHT = 5


class MazeGenerator:
    """Generates a random maze using the Recursive Backtracker algorithm.

    Attributes:
        width: Number of cells horizontally.
        height: Number of cells vertically.
        seed: Random seed for reproducibility.
        perfect: Whether the maze must be perfect.
        grid: 2D list representing the maze cells.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initializes the MazeGenerator.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
            seed: Random seed for reproducibility.
            perfect: Whether the maze must be perfect.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.grid: list[list[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]
        self.pattern_cells: set[tuple[int, int]] = set()
        sys.setrecursionlimit(self.width * self.height + 1000)

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        """Removes the wall between a cell and its neighbor.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
            direction: Direction (NORTH, EAST, SOUTH, WEST).
        """
        dx, dy = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        self.grid[y][x] = self.grid[y][x] & ~direction
        self.grid[ny][nx] = self.grid[ny][nx] & ~OPPOSITE[direction]

    def is_valid(self, x: int, y: int) -> bool:
        """Checks if the given coordinates are within the maze bounds.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if the coordinates are valid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_unvisited_neighbors(
        self, x: int, y: int, visited: list[list[bool]]
    ) -> list[tuple[int, int, int]]:
        """Returns a list of unvisited neighbors of the given cell.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
            visited: 2D list tracking visited cells.

        Returns:
            A list of tuples (nx, ny, direction) for each unvisited neighbor.
        """
        neighbors = []
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny) and not visited[ny][nx]:
                neighbors.append((nx, ny, direction))
        return neighbors

    def iterative_backtrack(
        self, start_x: int, start_y: int, visited: list[list[bool]]
    ) -> None:
        """Generates the maze using an iterative backtracking algorithm.

        Args:
            start_x: Column index of the starting cell.
            start_y: Row index of the starting cell.
            visited: 2D list tracking visited cells.
        """
        stack = [(start_x, start_y)]
        visited[start_y][start_x] = True

        while stack:
            x, y = stack[-1]
            neighbors = self.get_unvisited_neighbors(x, y, visited)

            if not neighbors:
                stack.pop()
            else:
                random.shuffle(neighbors)
                nx, ny, direction = neighbors[0]
                self.remove_wall(x, y, direction)
                visited[ny][nx] = True
                stack.append((nx, ny))

    def recursive_backtrack(
        self, x: int, y: int, visited: list[list[bool]]
    ) -> None:
        """Recursively generates the maze using the backtracking algorithm.

        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
            visited: 2D list tracking visited cells.
        """
        visited[y][x] = True

        neighbors = self.get_unvisited_neighbors(x, y, visited)
        random.shuffle(neighbors)

        for nx, ny, direction in neighbors:
            if not visited[ny][nx]:
                self.remove_wall(x, y, direction)
                self.recursive_backtrack(nx, ny, visited)

    def has_open_3x3(self, x: int, y: int) -> bool:
        """Checks if there is a 3x3 open area starting at (x, y).

        Args:
            x: Column index of the top-left cell.
            y: Row index of the top-left cell.

        Returns:
            True if a 3x3 open area exists, False otherwise.
        """
        for cy in range(y, y + 3):
            for cx in range(x, x + 3):
                if not self.is_valid(cx, cy):
                    return False
                cell = self.grid[cy][cx]
                if cx < x + 2 and cell & EAST:
                    return False
                if cy < y + 2 and cell & SOUTH:
                    return False
        return True

    def fix_open_areas(self) -> None:
        """Detects and fixes 3x3 open areas by adding a wall inside them."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.has_open_3x3(x, y):
                    # Add a south wall in the middle cell of the 3x3
                    mx, my = x + 1, y + 1
                    self.grid[my][mx] |= SOUTH
                    self.grid[my + 1][mx] |= NORTH

    def place_42(self) -> bool:
        """Places the '42' pattern in the maze using fully closed cells.

        Returns:
            True if the pattern was placed, False if the maze is too small.
        """
        if (self.width < PATTERN_42_WIDTH + 2
                or self.height < PATTERN_42_HEIGHT + 2):
            return False

        start_x = int((self.width - PATTERN_42_WIDTH) / 2)
        start_y = int((self.height - PATTERN_42_HEIGHT) / 2)

        for dx, dy in PATTERN_42:
            x = start_x + dx
            y = start_y + dy
            self.grid[y][x] = 15
            self.pattern_cells.add((x, y))

            for direction, (ndx, ndy) in DIRECTIONS.items():
                nx, ny = x + ndx, y + ndy
                if self.is_valid(nx, ny):
                    self.grid[ny][nx] |= OPPOSITE[direction]

        return True

    def make_imperfect(self) -> None:
        """Makes the maze imperfect by removing some random walls."""
        walls_to_remove = (self.width * self.height) // 10

        for _ in range(walls_to_remove):
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)
            direction = random.choice([EAST, SOUTH])
            if (x, y) not in self.pattern_cells:
                self.remove_wall(x, y, direction)

    def generate(self) -> list[list[int]]:
        """Generates the maze using the Recursive Backtracker algorithm.

        Returns:
            A 2D list representing the maze cells.
        """
        if self.seed is not None:
            random.seed(self.seed)

        visited: list[list[bool]] = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]
        if not self.place_42():
            raise ValueError("Maze is too small to fit the '42' pattern.")
        for x, y in self.pattern_cells:
            visited[y][x] = True
        self.recursive_backtrack(0, 0, visited)
        self.fix_open_areas()
        if not self.perfect:
            self.make_imperfect()
        return self.grid

    def solve(
        self, entry: tuple[int, int], exit: tuple[int, int]
    ) -> list[str]:
        """Finds the shortest path from entry to exit using BFS.

        Args:
            entry: The entry coordinates (x, y).
            exit: The exit coordinates (x, y).

        Returns:
            A list of directions (N, E, S, W) representing the shortest path.
        """

        queue: list[tuple[int, int]] = []
        queue.append(entry)

        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int, int]]] = {}
        came_from[entry] = None

        while queue:
            x, y = queue.pop(0)

            if (x, y) == exit:
                break

            for direction, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if not self.is_valid(nx, ny):
                    continue
                if (nx, ny) in came_from:
                    continue
                if self.grid[y][x] & direction:
                    continue
                came_from[(nx, ny)] = (x, y, direction)
                queue.append((nx, ny))

        if exit not in came_from:
            print("Exit is unreachable.")
            return []

        path: list[str] = []
        current: tuple[int, int] = exit
        dir_names = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}

        while came_from[current] is not None:
            result = came_from[current]
            if result is None:
                break
            cx, cy, direction = result
            path.append(dir_names[direction])
            current = (cx, cy)

        path.reverse()
        return path
