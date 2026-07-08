# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ccolnat <ccolnat@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 18:55:05 by ccolnat         #+#    #+#               #
#  Updated: 2026/06/25 18:55:06 by ccolnat         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from renderer import MazeRenderer
from mazegen.generator import MazeGenerator
import time
import os

COLORS = {
    1: "white",
    2: "cyan",
    3: "green",
    4: "red",
    5: "yellow",
    6: "magenta",
}


class MazeMenu:
    """Handles the interactive menu for the maze.

    Attributes:
        renderer: The MazeRenderer instance.
    """

    def __init__(self, renderer: MazeRenderer) -> None:
        """Initializes the MazeMenu.

        Args:
            renderer: The MazeRenderer instance.
        """
        self.renderer = renderer
        self.original_seed = self.renderer.maze.seed

    def check_color_choice(self, new_color: str) -> bool:
        """Checks if the chosen color is not already used by another element.

        Args:
            new_color: The new color chosen by the user.

        Returns:
            True if the new color is available, False otherwise.
        """
        current_colors = [
            self.renderer.get_wall_color().lower(),
            self.renderer.get_solve_path_color().lower(),
            self.renderer.get_pattern_color().lower(),
        ]

        if new_color in current_colors:
            print("Chosen color must be different from the current colors.")
            return False
        return True

    def run(self) -> None:
        """Runs the interactive menu."""
        os.system("clear")
        self.renderer.render()

        while True:
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Render maze with current settings")
            print("3. Show/Hide path from entry to exit")
            print("4. Change the maze color")
            print("5. Change the solve path color")
            print("6. Change the pattern color")
            print("7. Quit")
            print()

            choice = input("Choice (1-7): ").strip()

            if choice == "1":
                new_seed = int(time.time())
                self.renderer.maze = MazeGenerator(
                    self.renderer.maze.width,
                    self.renderer.maze.height,
                    seed=new_seed,
                    perfect=self.renderer.maze.perfect,
                )
                self.renderer.maze.generate()
                self.renderer.render()

            elif choice == "2":
                self.renderer.maze = MazeGenerator(
                    self.renderer.maze.width,
                    self.renderer.maze.height,
                    seed=self.original_seed,
                    perfect=self.renderer.maze.perfect,
                )
                self.renderer.maze.generate()
                self.renderer.render()

            elif choice == "3":
                self.renderer.show_path = not self.renderer.show_path
                self.renderer.render()

            elif choice == "4":
                os.system("clear")
                while True:
                    print("Wall colors:")
                    for i, name in COLORS.items():
                        print(f"{i}. {name}")
                    color_choice = input("Choose a color (1-6): ").strip()
                    if color_choice in [str(k) for k in COLORS.keys()]:
                        if self.check_color_choice(COLORS[int(color_choice)]):
                            self.renderer.set_wall_color(
                                COLORS[int(color_choice)])
                        self.renderer.render()
                        break
                    else:
                        print("Invalid choice, please enter "
                              "a number between 1 and 6.")

            elif choice == "5":
                os.system("clear")
                while True:
                    print("Solve path colors:")
                    for i, name in COLORS.items():
                        print(f"{i}. {name}")
                    color_choice = input("Choose a color (1-6): ").strip()
                    if color_choice in [str(k) for k in COLORS.keys()]:
                        if self.check_color_choice(COLORS[int(color_choice)]):
                            self.renderer.set_solve_path_color(
                                COLORS[int(color_choice)])
                        self.renderer.render()
                        break
                    else:
                        print("Invalid choice, please "
                              "enter a number between 1 and 6.")

            elif choice == "6":
                os.system("clear")
                while True:
                    print("Pattern colors:")
                    for i, name in COLORS.items():
                        print(f"{i}. {name}")
                    color_choice = input("Choose a color (1-6): ").strip()
                    if color_choice in [str(k) for k in COLORS.keys()]:
                        if self.check_color_choice(COLORS[int(color_choice)]):
                            self.renderer.set_pattern_color(
                                COLORS[int(color_choice)])
                        self.renderer.render()
                        break
                    else:
                        print("Invalid choice, please "
                              "enter a number between 1 and 6.")

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice, please enter between 1 and 7")
