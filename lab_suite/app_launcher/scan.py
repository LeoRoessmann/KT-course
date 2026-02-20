"""
Scannt lab_suite/labs/ und erkennt NiceGUI-Apps vs. Skript-Ordner.
Gruppierung nach Kapitel (Präfix aus Ordnernamen, z. B. 01_, 03_).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


# Unterordner, deren .py-Dateien nicht als eigenständige Skripte gelten
SCRIPT_EXCLUDE_DIRS = frozenset({"_core", "assignments", "templates"})


@dataclass
class LabEntry:
    """Ein Eintrag im Launcher: App, Skript oder reine Dokumentenabgabe (ohne Programmieraufgabe)."""
    kind: str  # "app" | "script" | "document"
    chapter: str  # z. B. "01", "03"
    folder_name: str  # Ordnername, z. B. 01_01_Signale_basics
    label: str  # Anzeigename
    # Für App: Modulname; für Skript: relativer Pfad; für document: leer (kein Start)
    run_target: str
    has_submissions_folder: bool


@dataclass
class ChapterGroup:
    """Kapitel mit zugehörigen Labs/Skripten."""
    chapter: str
    title: str  # z. B. "Kapitel 01"
    entries: list[LabEntry]


def _chapter_from_folder(folder_name: str) -> str:
    """Kapitel-Präfix aus Ordnernamen (z. B. 01_01_Signale_basics -> 01)."""
    if "_" in folder_name:
        return folder_name.split("_")[0]
    return folder_name[:2] if len(folder_name) >= 2 else folder_name


def _top_level_scripts(lab_dir: Path) -> list[str]:
    """Nur .py-Dateien direkt im Ordner (nicht in _core, assignments, …)."""
    scripts = []
    for f in lab_dir.iterdir():
        if not f.is_file() or f.suffix != ".py":
            continue
        if f.name.startswith("__"):
            continue
        scripts.append(f.name)
    return sorted(scripts)


def scan_labs(labs_root: Path) -> list[ChapterGroup]:
    """
    Scannt labs_root (lab_suite/labs) und liefert gruppierte Einträge.

    Pro Aufgabenordner wird immer mindestens eine Task-Card erzeugt:
    - NiceGUI-App (__main__.py) → ein Eintrag kind="app" (Web-Icon).
    - Keine App, aber Python-Skripte (oberste Ebene) → je Skript ein Eintrag kind="script" (Code-Icon).
    - Weder App noch Skripte → ein Eintrag kind="document" (Dokument-Icon): reine Dokumentenabgabe,
      gleiche submissions/-Nutzung, aber ohne „Starten“-Button.
    """
    if not labs_root.is_dir():
        return []

    groups: dict[str, list[LabEntry]] = {}
    for item in sorted(labs_root.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or item.name == "__pycache__":
            continue
        folder_name = item.name
        chapter = _chapter_from_folder(folder_name)
        submissions_dir = item / "submissions"
        has_submissions = submissions_dir.is_dir()

        if (item / "__main__.py").exists():
            entry = LabEntry(
                kind="app",
                chapter=chapter,
                folder_name=folder_name,
                label=folder_name,
                run_target=f"labs.{folder_name}",
                has_submissions_folder=has_submissions,
            )
            groups.setdefault(chapter, []).append(entry)
        else:
            scripts = _top_level_scripts(item)
            if scripts:
                for script_name in scripts:
                    entry = LabEntry(
                        kind="script",
                        chapter=chapter,
                        folder_name=folder_name,
                        label=f"{folder_name} / {script_name}",
                        run_target=f"labs/{folder_name}/{script_name}",
                        has_submissions_folder=has_submissions,
                    )
                    groups.setdefault(chapter, []).append(entry)
            else:
                # Keine Programmieraufgabe: trotzdem eine Karte für Dokumentenabgabe
                entry = LabEntry(
                    kind="document",
                    chapter=chapter,
                    folder_name=folder_name,
                    label=folder_name,
                    run_target="",
                    has_submissions_folder=has_submissions,
                )
                groups.setdefault(chapter, []).append(entry)

    result = []
    for ch in sorted(groups.keys()):
        result.append(ChapterGroup(
            chapter=ch,
            title=f"Kapitel {ch}",
            entries=groups[ch],
        ))
    return result
