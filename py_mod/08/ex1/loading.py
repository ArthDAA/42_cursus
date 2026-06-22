#!/usr/bin/env python3
import importlib
import sys
from typing import Any

REQUIRED: dict[str, str] = {
    "pandas": "2.x",
    "numpy": "1.x",
    "matplotlib": "3.x",
}


def check_dependencies() -> dict[str, Any]:
    print("Checking dependencies:")
    loaded: dict[str, Any] = {}
    missing: list[str] = []

    for pkg, _ in REQUIRED.items():
        try:
            mod = importlib.import_module(pkg)
            version: str = getattr(mod, "__version__", "unknown")
            print(f"[OK] {pkg} ({version})")
            loaded[pkg] = mod
        except ImportError:
            print(f"[MISSING] {pkg} - not installed")
            missing.append(pkg)

    if missing:
        print("\nMissing dependencies! Install them with:")
        print("  pip install -r requirements.txt")
        print("  -- or --")
        print("  poetry install")
        sys.exit(1)

    return loaded


def compare_pip_vs_poetry() -> None:
    print("\nDependency management comparison:")
    print("  pip:    pip install -r requirements.txt  (simple, no lock file)")
    print("  Poetry: poetry install                   (lock file, venv management)")


def analyze_matrix_data(mods: dict[str, Any]) -> None:
    np = mods["numpy"]
    pd = mods["pandas"]
    plt = mods["matplotlib.pyplot"] if "matplotlib.pyplot" in mods else None

    import matplotlib.pyplot as mplt

    print("\nAnalyzing Matrix data...")
    data: Any = np.random.randn(1000)
    print(f"Processing {len(data)} data points...")

    df: Any = pd.DataFrame({"signal": data})
    print(f"Mean: {df['signal'].mean():.4f}")
    print(f"Std:  {df['signal'].std():.4f}")

    print("Generating visualization...")
    fig, ax = mplt.subplots()
    ax.hist(data, bins=30, color="cyan", edgecolor="black")
    ax.set_title("Matrix Data Distribution")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    fig.savefig("matrix_analysis.png")
    mplt.close(fig)

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...\n")
    loaded_mods = check_dependencies()
    compare_pip_vs_poetry()
    analyze_matrix_data(loaded_mods)
