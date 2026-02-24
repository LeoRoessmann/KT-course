# assignments/user_template.py – Was steckt dahinter?

In dieser NiceGUI-App erweitern bzw. ergänzen Studierende den **eigenen Code** in **`assignments/user_template.py`**. Der Launcher-Button **EDIT** öffnet genau diese Datei im Editor.

## Rolle der Datei

- **GUI und App-Rahmen** liegen in `_core/` (Layout, Timer, Widgets). Die **fachliche Logik** (Huffman-Code, Baum, Ausgabe) lebt in **user_template.py**.
- Die GUI liefert Eingaben über **`gui_binding.get(key)`** (z. B. `get("my_text")` für den eingegebenen Text) und zeigt Ergebnisse über **`gui_binding.set(key, value)`** bzw. **`gui_binding.clear_markdown(key)`** und **`set(...)`** für Markdown-Boxen (z. B. Code-Tabelle, Codebaum).
- Die Zuordnung **Widget ↔ fachliche Größe** erfolgt über **User-IDs** aus dem Layout (z. B. `my_text`, `code_table`, `code_tree`). `SEMANTIC_BINDING` wird daraus befüllt.

## Wichtige Bausteine in user_template.py

- **`_node_label` / `_huffman_tree_ascii`:** Darstellung des Huffman-Baums als ASCII-Art (Blätter mit Symbol und Wahrscheinlichkeit, innere Knoten mit Summenwahrscheinlichkeit).
- **`_build_huffman_tree`:** Baut aus (Symbol, Häufigkeit) und zugehörigen Wahrscheinlichkeiten den Huffman-Baum (Bottom-up: zwei Knoten mit kleinsten Wahrscheinlichkeiten werden zusammengefasst).
- **`HuffmanCode`:** Klasse zur Berechnung der Huffman-Codewörter aus den Wahrscheinlichkeiten (`compute_code()`, `position()`, `characteristics_huffman_code()` für mittlere Codelänge).
- **`run_domain_logic()`:** Liest den Text aus der GUI (`get("my_text")`), berechnet Häufigkeiten und Wahrscheinlichkeiten, ruft `HuffmanCode` auf, schreibt Code-Tabelle und Baum in die Markdown-Widgets (`code_table`, `code_tree`) und gibt die mittlere Codelänge aus.
- **`solve_task()`:** Einstieg für die Fach-Aufgabe; wird von der App (z. B. aus user_callbacks oder Timer) aufgerufen und ruft `run_domain_logic()` auf.

## Was du anpassen kannst

- **Eigene Implementierung:** Huffman-Baum, Codewörter oder Ausgabe in `run_domain_logic()` anpassen oder ersetzen.
- **Zusätzliche Ausgaben:** Weitere `gui_binding.set(...)` oder `update_plot(...)` für weitere Widgets (sofern im Layout mit User-ID hinterlegt).
- **Timer:** Die App kann einen Timer nutzen und z. B. `timer_tick()` in diesem Modul aufrufen – für periodische Updates von Plots oder Logik.

Die Konsolenausgabe wird bei Bedarf parallel in **submissions/console_log.txt** geschrieben (Launcher: „Konsolenausgabe einfügen“), sofern das in der App vorgesehen ist.
