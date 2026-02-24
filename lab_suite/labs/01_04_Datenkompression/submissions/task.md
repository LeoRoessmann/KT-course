##### Aufgabe: Wort-Entropie mit word_dictionary.py

**Was macht das Skript?**  
`word_dictionary.py` liest **sampletext.txt** (im gleichen Ordner), zerlegt den Text in **Wörter** (Komma/Punkt werden ignoriert), zählt die Häufigkeit jedes Wortes und berechnet die **Entropie** pro Wort sowie die Gesamtentropie in bit/Byte. Die Ausgabe wird parallel in `submissions/console_log.txt` gespeichert.

---

**Arbeitsschritte:**

1. **Gleichen Text wie in Aufgabe 01_02 (Entropie) verwenden**  
   Verwende **dieselbe** Datei **sampletext.txt** wie in der Aufgabe *Entropie (entropy1.py)* (Lab `01_02_Informationstheorie`): Kopiere den Inhalt von `labs/01_02_Informationstheorie/sampletext.txt` nach `labs/01_04_Datenkompression/sampletext.txt`. So können wir die erzielte „Kompression“ (Entropie) bei **einzelnen Zeichen** (entropy1.py) und bei **zusammengefassten Wörtern** (word_dictionary.py) direkt vergleichen.

2. **Fragebogen öffnen** (optional zuerst)  
   Klicke auf „Fragebogen – Öffnen / Bearbeiten“, damit `answers.md` angelegt wird.

3. **Skript ausführen**  
   Starte `word_dictionary.py` über den Launcher (Button **Starten**). Die Ausgabe erscheint in der Konsole und in `submissions/console_log.txt`.

4. **Konsolenausgabe einfügen**  
   Klicke auf das **Merge-Symbol** („Konsolenausgabe in answers einfügen“). Der Inhalt von `console_log.txt` wird an deine `answers.md` angehängt.

5. **console_log kommentieren**  
   Öffne den Fragebogen erneut und **kommentiere** die eingefügte Ausgabe: Wie unterscheidet sich die Wort-Entropie von der Zeichen-Entropie (entropy1.py)? Was sagt die Entropie in Byte im Vergleich zur tatsächlichen Dateigröße aus?
