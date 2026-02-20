# KT-Lab App-Launcher

Übersicht aller Labs und Skripte in `lab_suite/labs/`, hierarchisch nach Kapitel. Ein Klick startet NiceGUI-Apps oder einzelne Python-Skripte.

## Start

Aus dem Ordner **lab_suite**:

```bash
python -m app_launcher
```

Browser öffnet sich typisch unter `http://localhost:8082`.

## Erkennung

Es wird **für jeden Unterordner** unter `labs/` mindestens eine **Task-Card** erzeugt. Drei Fälle:

- **NiceGUI-App:** Ordner enthält `__main__.py` → ein Eintrag mit **Web-Icon**, Start mit `python -m labs.<Ordnername>`.
- **Python-Skripte:** Ordner ohne `__main__.py`, dafür `.py`-Dateien auf oberster Ebene → je Skript ein Eintrag mit **Code-Icon** (`</>`), Start mit `python labs/<Ordner>/<Skript>.py`.
- **Nur Dokumentenabgabe:** Weder App noch Skripte → ein Eintrag mit **Dokument-Icon**; gleiche Nutzung von `submissions/` (Abgabe, Ordner, Drop-Zone), aber **kein „Starten“-Button** (keine Programmieraufgabe).

Die Hierarchie folgt dem Ordnernamen (z. B. `01_01_...` → Kapitel 01). Wenn `submissions/task.md` existiert, wird „Aufgabe anzeigen“ **einmal pro Aufgabenordner** in einer Expansion angezeigt.

## Submissions (Abgaben)

**Konvention:** Pro Lab ein Ordner **`submissions/`** im jeweiligen Lab-Verzeichnis. In jeder **Aufgabenkarte** (links neben „Starten“) gibt es bei Labs mit submissions-Ordner:
- **Ordner geöffnet (Icon):** Zeigt den Inhalt von submissions/ in einem Dialog (Dateiliste).
- **Ordner (Icon):** Öffnet den Ordner **submissions/** im **Windows-Explorer** (bzw. Dateimanager). So können Studierende Dateien ablegen, Stub-Dokumente bearbeiten oder entfernen und Abgaben vorbereiten. Dieselbe Aktion gibt es unter „E-mail Fallback Abgaben“ als Button „Ordner öffnen“.

Pro Aufgabenstellung (Lab) gibt es zusätzlich im Launcher eine Zeile **Abgabe (E-Mail-Fallback)** mit:

- **ZIP erstellen** – packt den Inhalt von `submissions/` in `abgabe_<Lab>_<datum>.zip` im gleichen Ordner.
- **Ordner öffnen** – öffnet den Dateimanager (Explorer/Finder) im `submissions/`-Ordner; Studierende können das ZIP auswählen und in die E-Mail ziehen.
- **E-Mail öffnen** – öffnet den Standard-Mail-Client mit Zieladresse und Betreff `[kt-assignment] ID=<Lab-Name>`.

**Zieladresse (repo-weit):** In **`lab_suite/submit_manifest.txt`** wird die Instructor-Adresse hinterlegt (eine Zeile, Format `submit_to_email=adresse@example.com`). Der Launcher liest diese Datei; ohne Eintrag ist „E-Mail öffnen“ deaktiviert.

**Abgabedatum pro Aufgabe:** Optional kann pro Lab eine Datei **`submissions/deadline.txt`** angelegt werden. Inhalt: **eine Zeile**, Datum im Format **`YYYY-MM-DD`** (z. B. `2025-04-15`). Der Launcher zeigt dann in der Aufgabenkarte links neben „Starten“ den Text **„Abgabe bis: DD.MM.YYYY“** an.

**Instructor-Modus (nur für Dozenten):** Wenn im Ordner **lab_suite** eine Datei **`.instructor_key`** existiert und nicht leer ist, erscheint pro Aufgabenkarte (mit submissions/) ein **Kalender-Icon**. Ein Klick öffnet einen Dialog mit Date-Picker: Abgabedatum wählen → „Übernehmen“ speichert in `deadline.txt` und lädt die Seite neu; „Löschen“ entfernt das Abgabedatum. Die Datei `.instructor_key` darf **nicht** ins Studenten-Repo exportiert werden (steht in `.gitignore` und im Export-Skript in der Ignore-Liste). Dozent: einmalig z. B. `echo kt-instructor > lab_suite/.instructor_key` anlegen.
