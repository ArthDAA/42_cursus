# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ccolnat <ccolnat@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 18:54:53 by ccolnat         #+#    #+#               #
#  Updated: 2026/06/25 18:54:54 by ccolnat         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
import sys
from config_parser import ConfigParser
from mazegen.generator import MazeGenerator
from renderer import MazeRenderer
from maze_writer import MazeWriter
from menu import MazeMenu


def main() -> None:
    """Main entry point of the program."""
    if len(sys.argv) != 2:
        raise TypeError("Missing configuration file. "
                        "Please provide exactly one argument.")

    parser = ConfigParser(sys.argv[1])
    config = parser.parse()

    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    entry_x, entry_y = map(int, config["ENTRY"].split(","))
    exit_x, exit_y = map(int, config["EXIT"].split(","))
    output_file = config["OUTPUT_FILE"]
    perfect = config["PERFECT"] == "True"
    seed = parser.get_seed()

    entry = (entry_x, entry_y)
    exit = (exit_x, exit_y)

    maze = MazeGenerator(
        width=width,
        height=height,
        seed=seed,
        perfect=perfect,
    )
    maze.generate()

    writer = MazeWriter(
        maze=maze,
        entry=entry,
        exit=exit,
        output_file=output_file,
    )
    writer.write()

    renderer = MazeRenderer(
        maze=maze,
        entry=entry,
        exit=exit,
    )

    menu = MazeMenu(renderer)
    try:
        menu.run()
    except KeyboardInterrupt:
        print("\nBye Bye")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
