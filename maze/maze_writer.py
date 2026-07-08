# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_writer.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ccolnat <ccolnat@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 18:55:03 by ccolnat         #+#    #+#               #
#  Updated: 2026/06/25 18:55:04 by ccolnat         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from mazegen.generator import MazeGenerator


class MazeWriter:
    """Writes the maze to a file in hexadecimal format.

    Attributes:
        maze: The MazeGenerator instance.
        entry: The entry coordinates (x, y).
        exit: The exit coordinates (x, y).
        output_file: The output file path.
    """

    def __init__(
        self,
        maze: MazeGenerator,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
    ) -> None:
        """Initializes the MazeWriter.

        Args:
            maze: The MazeGenerator instance.
            entry: The entry coordinates (x, y).
            exit: The exit coordinates (x, y).
            output_file: The output file path.
        """
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.output_file = output_file

    def write(self) -> None:
        """Writes the maze to the output file."""
        grid = self.maze.grid
        path = self.maze.solve(self.entry, self.exit)

        try:
            with open(self.output_file, "w") as f:
                for row in grid:
                    line = "".join(hex(cell)[2:].upper() for cell in row)
                    f.write(line + "\n")

                f.write("\n")

                f.write(f"{self.entry[0]},{self.entry[1]}\n")

                f.write(f"{self.exit[0]},{self.exit[1]}\n")

                f.write("".join(path) + "\n")

        except OSError as e:
            print(f"Error: could not write to file '{self.output_file}': {e}")
