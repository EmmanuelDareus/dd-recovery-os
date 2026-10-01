import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Core subdirectories
SRC_DIR = BASE_DIR / "src"
CORE_DIR = SRC_DIR / "core"
UTILS_DIR = SRC_DIR / "utils"
INTEGRATIONS_DIR = SRC_DIR / "integrations"
TESTS_DIR = BASE_DIR / "tests"

# Ensure directories exist if needed
for directory in [CORE_DIR, UTILS_DIR, INTEGRATIONS_DIR, TESTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)