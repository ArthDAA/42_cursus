#!/usr/bin/env python3
import sys
import os
import site


def is_in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def get_venv_name() -> str:
    return os.path.basename(sys.prefix)


def get_site_packages() -> str:
    packages: list[str] = site.getsitepackages()
    return packages[0] if packages else "unknown"


def main() -> None:
    if is_in_venv():
        print("MATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {get_venv_name()}")
        print(f"Environment Path: {sys.prefix}\n")
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")
        print("Package installation path:")
        print(get_site_packages())
    else:
        print("MATRIX STATUS: You're still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate  # On Unix")
        print(r"matrix_env\Scripts\activate  # On Windows")
        print("\nThen run this program again.")


if __name__ == "__main__":
    main()
