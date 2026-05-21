"""
Dump all project source files into a single .txt file.

Usage:
    python scripts/dump_project.py
"""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_DIR / "project_dump.txt"

EXCLUDED_DIRS = {
    ".venv", "venv", "__pycache__", ".git", ".mypy_cache",
    ".pytest_cache", "node_modules", ".tox", ".eggs",
    "data",
}

EXCLUDED_EXTENSIONS = {".pkl", ".pyc", ".pyo", ".so", ".egg", ".whl"}


def should_include(path: Path) -> bool:
    for part in path.relative_to(PROJECT_DIR).parts:
        if part in EXCLUDED_DIRS or part.startswith("."):
            return False
    if path.suffix in EXCLUDED_EXTENSIONS:
        return False
    return True


def main() -> None:
    files = sorted(
        f for f in PROJECT_DIR.rglob("*")
        if f.is_file() and should_include(f)
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for filepath in files:
            relative = filepath.relative_to(PROJECT_DIR)
            out.write(f"{'=' * 60}\n")
            out.write(f"FILE: {relative}\n")
            out.write(f"{'=' * 60}\n")
            try:
                out.write(filepath.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, PermissionError):
                out.write("[binary or unreadable file]\n")
            out.write("\n\n")

    print(f"Dumped {len(files)} files to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
