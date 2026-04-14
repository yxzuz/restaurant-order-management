from __future__ import annotations

import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_DIR = BASE_DIR / "app"

ROUTES_DIR = APP_DIR / "api" / "routes"
SERVICES_DIR = APP_DIR / "services"
REPOSITORIES_DIR = APP_DIR / "repositories"


def _python_files(directory: Path) -> list[Path]:
    return sorted(
        [
            file
            for file in directory.glob("*.py")
            if file.is_file() and file.name != "__init__.py"
        ]
    )


def _imports_for_file(file_path: Path) -> set[str]:
    tree = ast.parse(file_path.read_text(
        encoding="utf-8"), filename=str(file_path))
    imports: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports


def _normalize_app_imports(imports: set[str]) -> set[str]:
    return {imp for imp in imports if imp.startswith("app.")}


def test_routes_do_not_depend_on_repositories_directly():
    """Presentation layer should not bypass business layer."""
    violations: list[str] = []

    for file_path in _python_files(ROUTES_DIR):
        imports = _normalize_app_imports(_imports_for_file(file_path))
        bad = sorted(i for i in imports if i.startswith("app.repositories"))
        if bad:
            violations.append(f"{file_path.name}: {', '.join(bad)}")

    assert not violations, "\n".join(
        [
            "Routes must not import repositories directly (closed-layer rule).",
            *violations,
        ]
    )


def test_services_do_not_depend_on_routes():
    """Business layer should not depend on presentation layer."""
    violations: list[str] = []

    for file_path in _python_files(SERVICES_DIR):
        imports = _normalize_app_imports(_imports_for_file(file_path))
        bad = sorted(i for i in imports if i.startswith("app.api.routes"))
        if bad:
            violations.append(f"{file_path.name}: {', '.join(bad)}")

    assert not violations, "\n".join(
        [
            "Services must not import API route modules.",
            *violations,
        ]
    )


def test_repositories_do_not_depend_on_services_or_routes():
    """Data-access layer should stay isolated from upper layers."""
    violations: list[str] = []

    for file_path in _python_files(REPOSITORIES_DIR):
        imports = _normalize_app_imports(_imports_for_file(file_path))
        bad = sorted(
            i
            for i in imports
            if i.startswith("app.services") or i.startswith("app.api.routes")
        )
        if bad:
            violations.append(f"{file_path.name}: {', '.join(bad)}")

    assert not violations, "\n".join(
        [
            "Repositories must not import services or routes.",
            *violations,
        ]
    )


def test_services_avoid_direct_query_composition():
    """Fitness function for coupling: service layer should delegate query composition to repositories."""
    violations: list[str] = []

    for file_path in _python_files(SERVICES_DIR):
        text = file_path.read_text(encoding="utf-8")
        if ".query(" in text:
            violations.append(file_path.name)

    assert not violations, "\n".join(
        [
            "Services should not compose raw ORM queries directly.",
            "Move query logic into repositories.",
            f"Violations: {', '.join(violations)}",
        ]
    )
