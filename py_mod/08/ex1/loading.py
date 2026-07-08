#!/usr/bin/env python3
import importlib
import sys
from typing import Any

REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def check_dependencies() -> dict[str, Any]:
    print("Checking dependencies:")
    loaded: dict[str, Any] = {}
    missing: list[str] = []
    for pkg, role in REQUIRED.items():
        try:
            mod = importlib.import_module(pkg)
            version: str = getattr(mod, "__version__", "unknown")
            print(f"[OK] {pkg} ({version}) - {role} ready")
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


def compare_pip_vs_poetry(mods: dict[str, Any]) -> None:
    print("\nDependency management comparison:")
    print("Installed package versions:")
    for pkg, mod in mods.items():
        version: str = getattr(mod, "__version__", "unknown")
        print(f"  {pkg}=={version}")
    print("pip:    requirements.txt, flat list, no lock file")
    print("Poetry: pyproject.toml + poetry.lock, manages the venv")


def analyze_matrix_data(mods: dict[str, Any]) -> None:
    np = mods["numpy"]
    pd = mods["pandas"]
    plt: Any = importlib.import_module("matplotlib.pyplot")
    print("\nAnalyzing Matrix data...")
    data: Any = np.random.randn(1000)
    print(f"Processing {len(data)} data points...")
    df: Any = pd.DataFrame({"signal": data})
    print(f"Mean: {df['signal'].mean():.4f}")
    print(f"Std:  {df['signal'].std():.4f}")
    print("Generating visualization...")
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, color="cyan", edgecolor="black")
    ax.set_title("Matrix Data Distribution")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    fig.savefig("matrix_analysis.png")
    plt.close(fig)
    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")
    mods: dict[str, Any] = check_dependencies()
    compare_pip_vs_poetry(mods)
    analyze_matrix_data(mods)


if __name__ == "__main__":
    main()
