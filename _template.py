from pathlib import Path
import sys
import tomllib as _toml_loader
import tomli as _toml_loader
import toml as _toml_loader

#!/usr/bin/env python3
"""
Check pyproject.toml for name, version and description fields.

Saves as /C:/Users/AlexanderSchwarz/Desktop/PythonTemplate/_template.py
"""

# toml loader: prefer stdlib tomllib (3.11+), then tomli, then toml
try:

    def _load_toml(path: Path):
        with path.open("rb") as f:
            return _toml_loader.load(f)
except Exception:
    try:

        def _load_toml(path: Path):
            with path.open("rb") as f:
                return _toml_loader.load(f)
    except Exception:
        try:

            def _load_toml(path: Path):
                return _toml_loader.loads(path.read_text(encoding="utf-8"))
        except Exception:
            print("Missing TOML parser. Use Python 3.11+ or install 'tomli' (pip install tomli).", file=sys.stderr)
            sys.exit(3)


def find_pyproject(start: Path = None) -> Path | None:
    start = (Path(start) if start else Path.cwd()).resolve()
    for p in [start] + list(start.parents):
        candidate = p / "pyproject.toml"
        if candidate.is_file():
            return candidate
    return None


def extract_project_section(data: dict) -> tuple[str, dict] | tuple[None, None]:
    # PEP 621
    if isinstance(data.get("project"), dict):
        return "project", data["project"]
    # Poetry
    tool = data.get("tool")
    if isinstance(tool, dict):
        poetry = tool.get("poetry")
        if isinstance(poetry, dict):
            return "tool.poetry", poetry
        # flit uses tool.flit.metadata
        flit = tool.get("flit")
        if isinstance(flit, dict):
            metadata = flit.get("metadata")
            if isinstance(metadata, dict):
                return "tool.flit.metadata", metadata
    return None, None


def check_fields(section_name: str, section: dict) -> int:
    # prefer common keys; treat 'description' == 'desc' similarly
    name = section.get("name")
    version = section.get("version")
    description = section.get("description") or section.get("desc") or section.get("summary")

    missing = []
    if not name:
        missing.append("name")
    if not version:
        missing.append("version")
    if not description:
        missing.append("description/desc")

    print(f"Using section: {section_name}")
    if missing:
        print("Missing fields:", ", ".join(missing), file=sys.stderr)
        # show what is present
        print("Found values (may be empty):")
        print("  name   :", repr(name))
        print("  version:", repr(version))
        print("  desc   :", repr(description))
        return 2
    # success: print concise values
    print("name   :", name)
    print("version:", version)
    print("desc   :", description)
    return 0


def main() -> int:
    pyproject = find_pyproject()
    if not pyproject:
        print("pyproject.toml not found in current directory or any parent.", file=sys.stderr)
        return 4

    try:
        data = _load_toml(pyproject)
    except Exception as e:
        print(f"Failed to parse {pyproject}: {e}", file=sys.stderr)
        return 5

    section_name, section = extract_project_section(data)
    if not section:
        print("No recognized project section found (project, tool.poetry, tool.flit.metadata).", file=sys.stderr)
        return 6

    return check_fields(section_name, section)


if __name__ == "__main__":
    raise SystemExit(main())