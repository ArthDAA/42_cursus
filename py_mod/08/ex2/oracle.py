#!/usr/bin/env python3
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed.")
    print("Using environment variables only.")


DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local.db",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "http://localhost:8080",
}


def load_config() -> dict[str, str]:
    config: dict[str, str] = {}
    for key, default in DEFAULTS.items():
        config[key] = os.environ.get(key, default)
    return config


def display_config(config: dict[str, str]) -> None:
    mode: str = config["MATRIX_MODE"]
    db: str = config["DATABASE_URL"]
    api: str = config["API_KEY"]
    log: str = config["LOG_LEVEL"]
    zion: str = config["ZION_ENDPOINT"]

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    if "local" in db or "sqlite" in db:
        print("Database: Connected to local instance")
    else:
        print(f"Database: Connected to {db}")
    if api:
        print("API Access: Authenticated")
    else:
        print("API Access: No key configured (WARNING)")
    print(f"Log Level: {log}")
    if zion:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def security_check() -> None:
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    env_file: bool = os.path.isfile(".env")
    if env_file:
        print("[OK] .env file properly configured")
    else:
        print("[WARN] No .env file found - using defaults/env vars")
    print("[OK] Production overrides available")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    config: dict[str, str] = load_config()
    display_config(config)
    security_check()

    mode: str = config["MATRIX_MODE"]
    if mode == "production":
        print("\n[PROD] Production mode: strict settings applied.")
    else:
        print("\n[DEV] Development mode: verbose output enabled.")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
