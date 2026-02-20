"""
NiceGUI-Oberfläche des App-Launchers: hierarchische Liste, Start-Buttons, E-Mail-Fallback Submit.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from nicegui import ui

from .widgets import Banner
from .scan import ChapterGroup, LabEntry, scan_labs
from . import submit
from . import port_check

# lab_suite = Parent von app_launcher
LAB_SUITE_ROOT = Path(__file__).resolve().parent.parent
LABS_DIR = LAB_SUITE_ROOT / "labs"
INSTRUCTOR_KEY_PATH = LAB_SUITE_ROOT / ".instructor_key"


def _launch_app(entry: LabEntry) -> None:
    """Startet NiceGUI-App als Subprocess (python -m labs.xxx)."""
    cmd = [sys.executable, "-m", entry.run_target]
    try:
        subprocess.Popen(
            cmd,
            cwd=str(LAB_SUITE_ROOT),
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
        )
        ui.notify(f"App wird gestartet: {entry.run_target}", type="positive")
    except Exception as e:
        ui.notify(f"Starten fehlgeschlagen: {e}", type="negative")


def _launch_script(entry: LabEntry) -> None:
    """Startet Skript als Subprocess (python labs/.../file.py)."""
    cmd = [sys.executable, entry.run_target]
    try:
        subprocess.Popen(
            cmd,
            cwd=str(LAB_SUITE_ROOT),
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
        )
        ui.notify(f"Skript wird gestartet: {entry.run_target}", type="positive")
    except Exception as e:
        ui.notify(f"Starten fehlgeschlagen: {e}", type="negative")


def _launch(entry: LabEntry) -> None:
    if entry.kind == "app":
        _launch_app(entry)
    else:
        _launch_script(entry)


def _on_zip_create(folder_name: str) -> None:
    """ZIP aus submissions/ erstellen und ggf. Ordner öffnen."""
    ok, msg = submit.create_submissions_zip(LAB_SUITE_ROOT, folder_name)
    if ok:
        ui.notify(f"ZIP erstellt: {msg}", type="positive")
        submit.open_submissions_folder(LAB_SUITE_ROOT, folder_name)
    else:
        ui.notify(f"ZIP fehlgeschlagen: {msg}", type="negative")


def _on_open_folder(folder_name: str) -> None:
    """Dateimanager im submissions-Ordner öffnen."""
    ok, msg = submit.open_submissions_folder(LAB_SUITE_ROOT, folder_name)
    if ok:
        ui.notify("Ordner geöffnet.", type="positive")
    else:
        ui.notify(f"Ordner öffnen fehlgeschlagen: {msg}", type="negative")


def _make_drop_handler(folder_name: str):
    """Erstellt einen on_upload-Handler, der Dateien in labs/<folder_name>/submissions/ speichert."""

    async def handler(e):
        dest_dir = LABS_DIR / folder_name / "submissions"
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except OSError as err:
            ui.notify(f"Ordner nicht erstellbar: {err}", type="negative")
            return
        name = Path(e.file.name).name.strip() or "uploaded_file"
        if ".." in name or name.startswith("/"):
            ui.notify("Ungültiger Dateiname.", type="negative")
            return
        path = dest_dir / name
        try:
            await e.file.save(str(path))
            ui.notify(f"Gespeichert: {name} → submissions/", type="positive")
        except Exception as err:
            ui.notify(f"Speichern fehlgeschlagen: {err}", type="negative")

    return handler


def _list_submissions(folder_name: str) -> list[tuple[str, int]]:
    """Listet labs/<folder_name>/submissions/; liefert [(Dateiname, Größe in Bytes), ...], sortiert nach Name."""
    path = LABS_DIR / folder_name / "submissions"
    if not path.is_dir():
        return []
    result: list[tuple[str, int]] = []
    try:
        for f in sorted(path.iterdir()):
            if f.is_file():
                result.append((f.name, f.stat().st_size))
    except OSError:
        pass
    return result


def _show_submissions_dialog(folder_name: str) -> None:
    """Öffnet einen Dialog mit dem Inhalt des submission-Ordners (Dateiliste + Größe)."""
    items = _list_submissions(folder_name)
    with ui.dialog() as d, ui.card().classes("q-pa-md min-w-[280px]"):
        ui.label(f"Inhalt: submissions/").classes("text-subtitle2 text-weight-medium")
        ui.label(folder_name).classes("text-caption text-grey-7 q-mb-sm")
        if not items:
            ui.label("(Ordner leer oder nicht vorhanden)").classes("text-body2 text-grey")
        else:
            with ui.column().classes("w-full gap-0"):
                for name, size in items:
                    size_str = f"{size:,} B" if size < 1024 else f"{size / 1024:.1f} KB"
                    with ui.row().classes("items-center q-gutter-sm full-width"):
                        ui.icon("insert_drive_file", size="sm").classes("text-grey-7")
                        ui.label(name).classes("flex-grow text-body2")
                        ui.label(size_str).classes("text-caption text-grey-7")
        ui.button("Schließen", on_click=d.close).props("flat color=primary").classes("q-mt-sm")
    d.open()


def _is_instructor_mode() -> bool:
    """True, wenn die Instructor-Key-Datei existiert und nicht leer ist (Key nicht an Studierende exportieren)."""
    if not INSTRUCTOR_KEY_PATH.is_file():
        return False
    try:
        return bool(INSTRUCTOR_KEY_PATH.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _read_deadline_iso(folder_name: str) -> str | None:
    """Liest deadline.txt, gibt YYYY-MM-DD zurück oder None."""
    path = LABS_DIR / folder_name / "submissions" / "deadline.txt"
    if not path.is_file():
        return None
    try:
        line = path.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if len(line) >= 10 and line[4] == "-" and line[7] == "-":
            return line[:10]
    except Exception:
        pass
    return None


def _write_deadline(folder_name: str, date_iso: str) -> bool:
    """Schreibt YYYY-MM-DD in submissions/deadline.txt. Erstellt submissions/ bei Bedarf."""
    dest_dir = LABS_DIR / folder_name / "submissions"
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / "deadline.txt").write_text(date_iso.strip()[:10] + "\n", encoding="utf-8")
        return True
    except OSError:
        return False


def _deadline_reminder(folder_name: str) -> tuple[str, str] | None:
    """
    Berechnet aus deadline.txt den Hinweistext und die Farbe für die Task-Card.
    Rückgabe: (Text, Quasar-Farbklasse) oder None, wenn kein gültiges Abgabedatum.
    - Noch nicht fällig: "Abgabe in X Tagen" (grün wenn > 3 Tage, bernstein/amber wenn ≤ 3 Tage).
    - Heute fällig: "Abgabe heute" (bernstein/amber).
    - Überfällig: "Abgabe seit X Tagen" (rot).
    """
    from datetime import date

    iso = _read_deadline_iso(folder_name)
    if not iso or len(iso) < 10:
        return None
    try:
        deadline = date.fromisoformat(iso[:10])
    except ValueError:
        return None
    today = date.today()
    days = (deadline - today).days
    if days > 3:
        return (f"Abgabe in {days} Tagen", "text-green")
    if days > 0:
        return (f"Abgabe in {days} Tagen", "text-amber-8")
    if days == 0:
        return ("Abgabe heute", "text-amber-8")
    return (f"Abgabe seit {-days} Tagen", "text-red")


def _read_task_done(folder_name: str) -> str | None:
    """
    Liest labs/<folder_name>/submissions/task_done.txt (eine Zeile: „Abgabe am DD.MM.YYYY“).
    Gibt das Datum „DD.MM.YYYY“ zurück oder None. State ist session-übergreifend und per Git für den Dozenten sichtbar.
    """
    path = LABS_DIR / folder_name / "submissions" / "task_done.txt"
    if not path.is_file():
        return None
    try:
        line = path.read_text(encoding="utf-8").strip().splitlines()
        if not line:
            return None
        text = line[0].strip()
        if text.startswith("Abgabe am "):
            return text.replace("Abgabe am ", "").strip()
    except Exception:
        pass
    return None


def _write_task_done(folder_name: str) -> bool:
    """Schreibt „Abgabe am DD.MM.YYYY“ in submissions/task_done.txt. Erstellt submissions/ bei Bedarf."""
    from datetime import date

    dest_dir = LABS_DIR / folder_name / "submissions"
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        today = date.today().strftime("%d.%m.%Y")
        (dest_dir / "task_done.txt").write_text(f"Abgabe am {today}\n", encoding="utf-8")
        return True
    except OSError:
        return False


def _clear_task_done(folder_name: str) -> bool:
    """Entfernt submissions/task_done.txt."""
    path = LABS_DIR / folder_name / "submissions" / "task_done.txt"
    try:
        if path.is_file():
            path.unlink()
        return True
    except OSError:
        return False


def _read_deadline(folder_name: str) -> str | None:
    """
    Liest labs/<folder_name>/submissions/deadline.txt (eine Zeile: YYYY-MM-DD).
    Gibt das Datum als Anzeigestring (DD.MM.YYYY) zurück oder None, wenn keine Datei/ungültig.
    """
    path = LABS_DIR / folder_name / "submissions" / "deadline.txt"
    if not path.is_file():
        return None
    try:
        line = path.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if not line:
            return None
        # ISO YYYY-MM-DD → DD.MM.YYYY
        parts = line.split("-")
        if len(parts) == 3 and len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2:
            y, m, d = parts[0], parts[1], parts[2]
            if y.isdigit() and m.isdigit() and d.isdigit():
                return f"{d}.{m}.{y}"
    except Exception:
        pass
    return None


def _show_deadline_picker_dialog(folder_name: str) -> None:
    """Öffnet Dialog mit Kalender zur Auswahl des Abgabedatums (nur im Instructor-Modus)."""
    from datetime import date as date_type

    initial = _read_deadline_iso(folder_name) or date_type.today().isoformat()
    with ui.dialog() as d, ui.card().classes("q-pa-md min-w-[300px]"):
        ui.label("Abgabedatum setzen").classes("text-subtitle2 text-weight-medium")
        ui.label(folder_name).classes("text-caption text-grey-7 q-mb-sm")
        picker = ui.date(value=initial, mask="YYYY-MM-DD").classes("w-full")
        with ui.row().classes("q-mt-md q-gutter-sm"):
            ui.button("Abbrechen", on_click=d.close).props("flat")
            ui.button("Löschen", on_click=lambda: _apply_deadline_and_close(folder_name, None, d)).props("flat color=negative")
            ui.button("Übernehmen", on_click=lambda: _apply_deadline_and_close(folder_name, picker, d)).props("flat color=primary")
    d.open()


def _apply_deadline_and_close(folder_name: str, picker, d) -> None:
    """Schreibt gewähltes Datum in deadline.txt (oder löscht Datei), schließt Dialog, lädt Seite neu."""
    if picker is not None:
        val = getattr(picker, "value", None)
        date_str = (str(val)[:10] if val else "").strip()
        if not date_str or len(date_str) < 10:
            ui.notify("Bitte ein gültiges Datum wählen.", type="warning")
            return
        if not _write_deadline(folder_name, date_str):
            ui.notify("Speichern fehlgeschlagen.", type="negative")
            return
        ui.notify(f"Abgabe bis: {date_str} gespeichert.", type="positive")
    else:
        path = LABS_DIR / folder_name / "submissions" / "deadline.txt"
        try:
            if path.is_file():
                path.unlink()
            ui.notify("Abgabedatum entfernt.", type="positive")
        except OSError:
            ui.notify("Löschen fehlgeschlagen.", type="negative")
    d.close()
    ui.run_javascript("window.location.reload()")


def _read_task_md(folder_name: str) -> str:
    """Liest labs/<folder_name>/submissions/task.md; leere Zeichenkette falls nicht vorhanden."""
    path = LABS_DIR / folder_name / "submissions" / "task.md"
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _task_markdown_extras() -> list[str]:
    """Extras für ui.markdown (LaTeX nur wenn latex2mathml verfügbar)."""
    extras = ["fenced-code-blocks", "tables"]
    try:
        import latex2mathml.converter  # noqa: F401
        extras.append("latex")
    except ImportError:
        pass
    return extras


EXPANSION_STATE_PATH = LAB_SUITE_ROOT / "launcher_expansion_state.json"


def _read_expansion_state() -> dict[str, bool]:
    """Liest den gespeicherten Open/Closed-State der Hauptkapitel-Expansions (session-übergreifend)."""
    if not EXPANSION_STATE_PATH.is_file():
        return {}
    try:
        import json

        data = json.loads(EXPANSION_STATE_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {k: bool(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def _write_expansion_state(state: dict[str, bool]) -> None:
    """Speichert den Open/Closed-State der Hauptkapitel-Expansions."""
    try:
        import json

        EXPANSION_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _on_expansion_change(title: str, is_open: bool) -> None:
    """Aktualisiert den gespeicherten State für ein Kapitel und schreibt die Datei."""
    state = _read_expansion_state()
    state[title] = is_open
    _write_expansion_state(state)


def _group_entries_by_folder(entries: list[LabEntry]) -> list[tuple[str, list[LabEntry]]]:
    """Gruppiert Einträge nach folder_name, Reihenfolge wie in entries (erstes Vorkommen)."""
    order: list[str] = []
    groups: dict[str, list[LabEntry]] = {}
    for e in entries:
        if e.folder_name not in groups:
            order.append(e.folder_name)
            groups[e.folder_name] = []
        groups[e.folder_name].append(e)
    return [(fn, groups[fn]) for fn in order]


# Nur 8081 prüfen – 8082 ist der Launcher selbst; Freigabe von 8082 würde den Launcher beenden
LAB_APP_PORT = 8081
PORT_CHECK_INTERVAL = 1.0  # Sekunden


def _fill_port_status_content(container: ui.column) -> None:
    """Füllt den übergebenen Container mit dem aktuellen Port-8081-Status (für Timer-Aktualisierung)."""
    container.clear()
    with container:
        pids = port_check.get_pids_on_port(LAB_APP_PORT)
        if not pids:
            with ui.row().classes("items-center q-gutter-sm"):
                ui.icon("check_circle", size="sm").classes("text-green-7")
                ui.label("Port 8081: frei").classes("text-body2 text-weight-medium text-green-8")
            ui.label("Labs können auf Port 8081 starten. Bei „Socket bereits verwendet“ diese Expansion öffnen.").classes(
                "text-caption text-grey-7 q-mt-xs"
            )
        else:
            pid = pids[0]
            name = port_check.get_process_name(pid) or "?"
            with ui.row().classes("items-center q-gutter-sm"):
                ui.icon("warning", size="sm").classes("text-amber-8")
                ui.label("Port 8081: belegt").classes("text-body2 text-weight-medium text-amber-9")
            ui.label(
                "Belegt kann bedeuten: (1) Ein Lab läuft regulär – dann nichts tun. "
                "(2) Port ist verwaist (z. B. nach Absturz oder Doppelstart) – dann unten „Port freigeben“ nutzen, "
                "damit ein neues Lab starten kann."
            ).classes("text-caption text-grey-8 q-my-xs")
            with ui.row().classes("items-center q-gutter-sm full-width q-mt-sm"):
                ui.label(f"Belegt von: {name} (PID {pid})").classes("text-caption text-grey-7 flex-grow")
                ui.button("Port freigeben", on_click=lambda pid_to_kill=pid: _on_free_port(LAB_APP_PORT, pid_to_kill)).props(
                    "flat dense color=amber-8"
                )


def _build_port_status_card() -> None:
    """Zeigt in einer (standardmäßig geschlossenen) Expansion den Status von Port 8081; Inhalt wird im Sekundentakt aktualisiert."""
    with ui.expansion("Port 8081 prüfen (nur bei Startproblemen öffnen)", value=False).classes("w-full q-mb-md"):
        port_content = ui.column().classes("w-full")
        _fill_port_status_content(port_content)
        ui.timer(PORT_CHECK_INTERVAL, lambda: _fill_port_status_content(port_content), once=False)


def _on_free_port(port: int, pid: int) -> None:
    """Beendet den Prozess auf dem Port und lädt die Seite neu."""
    if port_check.kill_process(pid):
        ui.notify(f"Port {port} freigegeben (Prozess {pid} beendet).", type="positive")
        ui.run_javascript("window.location.reload()")
    else:
        ui.notify("Port konnte nicht freigegeben werden (evtl. fehlen Rechte).", type="negative")


def build_ui() -> None:
    """Baut die Launcher-UI: Kapitel-Gruppen, Einträge mit Start-Button, Submit-Zeile pro Lab."""
    chapters = scan_labs(LABS_DIR)
    if not chapters:
        ui.label("Keine Labs gefunden. Bitte lab_suite/labs/ prüfen.").classes("text-weight-medium")
        return

    instructor_mode = _is_instructor_mode()
    submit_email = submit.read_submit_to_email(LAB_SUITE_ROOT)

    ui.label("Verfügbare Labs und Skripte").classes("text-h5 q-mb-md")
    ui.label("Klicke auf „Starten“, um eine App (Browser) oder ein Skript (Konsole/Matplotlib) zu starten.").classes(
        "text-body2 text-grey-7 q-mb-lg"
    )

    expansion_state = _read_expansion_state()
    for group in chapters:
        # State pro Kapitel: gespeichert in launcher_expansion_state.json, default offen (True)
        initial_open = expansion_state.get(group.title, True)
        with ui.expansion(group.title, value=initial_open).classes("w-full launcher-chapter-expansion") as chapter_exp:
            def _chapter_expansion_handler(e, title=group.title):
                is_open = getattr(e, "value", None)
                if is_open is None and getattr(e, "args", None) and len(e.args) > 0:
                    is_open = e.args[0]
                _on_expansion_change(title, bool(is_open) if is_open is not None else True)

            chapter_exp.on_value_change(_chapter_expansion_handler)
            with ui.column().classes("w-full bg-grey-2 rounded-borders q-pa-md"):
                for folder_name, folder_entries in _group_entries_by_folder(group.entries):
                    task_done_date = _read_task_done(folder_name)
                    card_bg = "bg-green-1" if task_done_date else "bg-white"
                    # Leicht schattierter Container pro Aufgabenblock (Einträge + Aufgabe); hellgrün wenn als erledigt markiert
                    with ui.card().classes(f"w-full q-mb-md rounded-borders {card_bg}").style("box-shadow: 0 1px 3px rgba(0,0,0,0.08)"):
                        deadline_str = _read_deadline(folder_name)
                        for entry in folder_entries:
                            with ui.row().classes("items-center q-gutter-sm full-width q-mb-xs"):
                                if entry.kind == "app":
                                    ui.icon("web", size="sm").classes("text-primary")
                                elif entry.kind == "script":
                                    ui.icon("code", size="sm").classes("text-secondary")
                                else:
                                    ui.icon("description", size="sm").classes("text-grey-7").tooltip(
                                        "Dokumentenabgabe (keine Programmieraufgabe)"
                                    )
                                ui.label(entry.label).classes("flex-grow")
                                if entry.has_submissions_folder:
                                    ui.badge("submissions/", color="green").classes("text-caption")
                                    ui.button(
                                        icon="folder_open",
                                        on_click=lambda fn=folder_name: _show_submissions_dialog(fn),
                                    ).props("flat dense round color=secondary").tooltip("Inhalt von submissions/ anzeigen")
                                    ui.button(
                                        icon="folder",
                                        on_click=lambda fn=folder_name: _on_open_folder(fn),
                                    ).props("flat dense round color=secondary").tooltip(
                                        "submissions/ im Explorer öffnen (Dateien hinzufügen, Stub-Dokumente bearbeiten oder entfernen)"
                                    )
                                    if instructor_mode:
                                        ui.button(
                                            icon="edit_calendar",
                                            on_click=lambda fn=folder_name: _show_deadline_picker_dialog(fn),
                                        ).props("flat dense round color=primary").tooltip("Abgabedatum setzen (Instructor)")
                                if deadline_str:
                                    ui.label(f"Abgabe bis: {deadline_str}").classes(
                                        "text-caption text-weight-medium text-grey-8"
                                    )
                                    reminder = _deadline_reminder(folder_name)
                                    if reminder:
                                        msg, color = reminder
                                        ui.label(msg).classes(f"text-caption text-weight-medium {color}")
                                if entry.kind != "document":
                                    ui.button("Starten", on_click=lambda e=entry: _launch(e)).props("flat dense color=primary")
                        # Drop-Zone für submissions/ (nur wenn Lab submissions-Ordner hat; grünes Badge signalisiert das)
                        if any(e.has_submissions_folder for e in folder_entries):
                            ui.upload(
                                on_upload=_make_drop_handler(folder_name),
                                label="Dateien hier ablegen → submissions/",
                                auto_upload=True,
                                multiple=True,
                            ).classes("w-full q-mt-xs").props("flat bordered")
                        # Aufgabe nach dem letzten Eintrag des Blocks
                        task_content = _read_task_md(folder_name)
                        if task_content.strip():
                            with ui.expansion("Aufgabe anzeigen", value=False).classes("w-full q-ml-sm q-mt-xs q-mb-sm"):
                                extras = _task_markdown_extras()
                                ui.markdown(task_content, extras=extras).classes("q-pa-sm bg-white rounded-borders")

                        # SUBMIT-Checkbox: Aufgabe als erledigt markieren (State in submissions/task_done.txt, session-übergreifend + per Git sichtbar)
                        def _on_submit_check(folder: str, value: bool) -> None:
                            if value:
                                if not _write_task_done(folder):
                                    ui.notify("Speichern fehlgeschlagen.", type="negative")
                                    return
                                ui.notify("Als erledigt gespeichert (Abgabe am " + _read_task_done(folder) + ").", type="positive")
                            else:
                                # Uncheck: task_done.txt löschen, Karte wird nach Reload wieder weiß
                                _clear_task_done(folder)
                                ui.notify("Markierung entfernt.", type="info")
                            ui.run_javascript("window.location.reload()")

                        with ui.row().classes("items-center q-gutter-sm full-width q-mt-sm q-pt-sm border-top"):
                            # on_change muss im Konstruktor übergeben werden (NiceGUI registriert es sonst nicht).
                            # fn=folder_name bindet den Ordner pro Karte. Neuer Wert aus e.args oder e.sender.value.
                            def _submit_check_handler(e, fn=folder_name):
                                val = True
                                if getattr(e, "args", None) is not None and len(e.args) > 0:
                                    val = bool(e.args[0])
                                elif getattr(e, "sender", None) is not None and hasattr(e.sender, "value"):
                                    val = bool(e.sender.value)
                                _on_submit_check(fn, val)

                            submit_check = ui.checkbox(
                                "SUBMIT (als erledigt markieren)",
                                value=bool(task_done_date),
                                on_change=_submit_check_handler,
                            )
                            if task_done_date:
                                ui.label(f"Abgabe am {task_done_date}").classes("text-caption text-weight-medium text-green-8")

                # Pro Lab (eindeutige folder_name) eine Submit-Zeile: ZIP, Ordner öffnen, E-Mail – unter Expansion (default zu)
                unique_folders = sorted({e.folder_name for e in group.entries})
                if unique_folders:
                    with ui.expansion("E-mail Fallback Abgaben", value=False).classes("w-full q-mt-sm"):
                        ui.label("Abgabe (E-Mail-Fallback)").classes("text-caption text-grey-7 q-mb-xs")
                        for folder_name in unique_folders:
                            with ui.row().classes("items-center q-gutter-sm full-width q-mb-xs"):
                                ui.label(folder_name).classes("text-body2 flex-grow")
                                ui.button("ZIP erstellen", on_click=lambda fn=folder_name: _on_zip_create(fn)).props(
                                    "flat dense color=secondary"
                                )
                                ui.button("Ordner öffnen", on_click=lambda fn=folder_name: _on_open_folder(fn)).props(
                                    "flat dense color=secondary"
                                )
                                mailto_url = submit.build_mailto_url(submit_email, folder_name)
                                if mailto_url:
                                    ui.link("E-Mail öffnen", mailto_url).props("flat dense color=secondary").classes(
                                        "text-secondary"
                                    )
                                else:
                                    ui.label("(submit_to_email in submit_manifest.txt fehlt)").classes("text-caption text-grey")

    ui.separator().classes("q-my-lg")
    with ui.card().classes("w-full bg-blue-1"):
        ui.label("Abgaben (Submissions)").classes("text-subtitle1 text-weight-medium")
        ui.label(
            "Pro Lab: Ordner submissions/. ZIP erstellen → Ordner öffnen → ZIP in die geöffnete E-Mail ziehen und senden. "
            "Zieladresse: lab_suite/submit_manifest.txt (submit_to_email=…)."
        ).classes("text-body2")
        ui.label("Pfad: lab_suite/labs/<Lab-Name>/submissions/").classes("text-caption text-grey-7")


def run(port: int = 8082, title: str = "KT-Lab Launcher") -> None:
    """Startet die NiceGUI-App (Launcher)."""

    @ui.page("/")
    def index():
        # Größere Schrift für Kapitel-Expansion-Überschriften; Schatten-Hintergrund wird per Klasse gesetzt
        ui.add_head_html(
            """
            <style>
            /* Sticky: Banner + Port-Check bleiben beim Scrollen sichtbar */
            .launcher-sticky-header { position: sticky; top: 0; z-index: 10; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
            /* Nur die äußere Kapitel-Expansion: Header-Label groß */
            .launcher-chapter-expansion .q-expansion-item__container > .q-item .q-item__label { font-size: 1.35rem; font-weight: 600; }
            .launcher-chapter-expansion .q-expansion-item__container > .q-item { min-height: 48px; }
            /* Innere Expansionen (Aufgabe anzeigen, E-mail Fallback): blau, geringere Signifikanz */
            .launcher-chapter-expansion .q-expansion-item__content .q-expansion-item .q-item__label { font-size: 1rem; font-weight: normal; color: #1565c0; }
            </style>
            """
        )
        with ui.column().classes("q-pa-lg w-full"):
            with ui.column().classes("launcher-sticky-header q-pa-lg w-full rounded-borders q-mb-md"):
                Banner(
                    text1=title,
                    text2="Labs starten · Aufgaben einsehen",
                    text3="Abgaben senden",
                    height="80px",
                ).classes("w-full")
                _build_port_status_card()
            build_ui()

    ui.run(port=port, title=title, reload=False)
