# Was macht huffman.py?

Das Skript berechnet **Huffman-Codes** für eine Zeichenkette:

1. **Eingabe:** Eine Zeichenkette wird zur Laufzeit abgefragt (`input(...)`).
2. **Häufigkeit:** Es zählt die Häufigkeit jedes Zeichens und sortiert sie absteigend.
3. **Baum:** Aus den Häufigkeiten wird ein **Huffman-Baum** gebaut (Bottom-up: die zwei seltensten Symbole werden zu einem Knoten zusammengefasst, bis nur noch ein Wurzelknoten übrig ist).
4. **Codes:** Aus dem Baum werden die binären Codewörter abgeleitet (z. B. linke Kante = 0, rechte = 1).
5. **Ausgabe:** In der Konsole erscheinen die Zeichen mit zugehörigem Huffman-Code; die Ausgabe wird parallel in `submissions/console_log.txt` geschrieben (für „Konsolenausgabe einfügen“ im Launcher).

Am Ende hält eine Endlosschleife die Konsole offen.
