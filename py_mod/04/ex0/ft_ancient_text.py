import sys
import typing

try:
    accfold: str = sys.argv[1]
    print(
        "=== Cyber Archives Recovery ===\n"
        f"Accessing file '{accfold}'"
    )
    try:
        f = open(accfold, "r")
        contenu = f.read()
        print(
            "---\n\n"
            f"{contenu}\n\n"
            "---\n"
            f"File '{accfold}' closed."
        )
        f.close()
    except Exception as e:
        print(
            f"Error opening file '{accfold}': {e}"
        )


except IndexError as e:
    print("Usage: ft_ancient_text.py <file>")