# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_parser.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ccolnat <ccolnat@student.42.fr>           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/25 18:54:57 by ccolnat         #+#    #+#               #
#  Updated: 2026/06/25 18:54:58 by ccolnat         ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from typing import Optional
import os


class ConfigParser:
    """Parses and validates the maze configuration file.

    Attributes:
        filepath: Path to the configuration file.
        config: Dictionary containing the parsed configuration.
    """

    REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY",
                     "EXIT", "OUTPUT_FILE", "PERFECT"]

    def __init__(self, filepath: str) -> None:
        """Initializes the ConfigParser with the given file path.

        Args:
            filepath: Path to the configuration file.
        """
        self.filepath = filepath
        self.config: dict[str, str] = {}

    def parse(self) -> dict[str, str]:
        """Reads and parses the configuration file.

        Returns:
            A dictionary with all configuration key-value pairs.
        """
        try:
            with open(self.filepath) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise ValueError(f"Invalid line in config: '{line}'")
                    key, value = line.split("=", 1)
                    if "#" in value:
                        value, comment = value.split("#", 1)
                    self.config[key.strip()] = value.strip()
                    self.unknown_key(key.strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{self.filepath}' not found")
        self.validate()
        return self.config

    def unknown_key(self, key: str) -> None:
        """Validates that the key is allowed.
        Raises KeyError if the key is not in REQUIRED_KEYS or SEED."""
        if key not in self.REQUIRED_KEYS and key != "SEED":
            raise KeyError(f"Unknown key '{key}' in config file")

    def validate(self) -> None:
        """Validates that all required keys are present and
        values are correct."""
        for key in self.REQUIRED_KEYS:
            if key not in self.config:
                raise KeyError(f"Missing key '{key}' in config file")
        self.validate_dimensions()
        self.validate_coordinates()
        self.validate_perfect()
        self.validate_output_file()

    def validate_dimensions(self) -> None:
        """Validates WIDTH and HEIGHT are positive integers."""

        for key in ["WIDTH", "HEIGHT"]:
            try:
                value = int(self.config[key])
                if value <= 0:
                    raise ValueError(f"'{key}' must be a positive integer")
                if value > 50:
                    raise ValueError(f"'{key}' must be lower than 50")
            except ValueError as e:
                raise ValueError(f"{e}")

    def validate_coordinates(self) -> None:
        """Validates ENTRY and EXIT coordinates are inside the maze bounds."""
        width = int(self.config["WIDTH"])
        height = int(self.config["HEIGHT"])

        for key in ["ENTRY", "EXIT"]:
            try:
                val_x, val_y = self.config[key].split(",")
                x, y = int(val_x.strip()), int(val_y.strip())
            except Exception:
                raise ValueError(f"'{key}' must be in the format "
                                 "'x,y' with integer values")
            else:
                if not (0 <= x < width and 0 <= y < height):
                    raise ValueError(f"Error: '{key}' coordinates "
                                     "are invalid or out of bounds")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("ENTRY and EXIT must be different")

    def validate_perfect(self) -> None:
        """Validates that PERFECT is a boolean value."""
        if self.config["PERFECT"] not in ["True", "False"]:
            raise ValueError("'PERFECT' must be 'True' or 'False'")

    def get_seed(self) -> Optional[int]:
        """Returns the seed value if provided, otherwise None.

        Returns:
            The seed as an integer, or None if not set.
        """
        if "SEED" in self.config:
            try:
                return int(self.config["SEED"])
            except ValueError:
                raise ValueError("'SEED' must be an integer")
        return None

    def validate_output_file(self) -> None:
        """Validates that the output file path is valid."""
        output_file = self.config["OUTPUT_FILE"]

        if not output_file:
            raise ValueError("'OUTPUT_FILE' cannot be empty")

        if os.path.abspath(output_file) == os.path.abspath(self.filepath):
            raise ValueError(
                "'OUTPUT_FILE' cannot be the same as the config file")

        if not output_file.endswith(".txt"):
            raise ValueError("'OUTPUT_FILE' must end with .txt")
