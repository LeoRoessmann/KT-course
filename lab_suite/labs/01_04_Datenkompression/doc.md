# Was macht word_dictionary.py?

Das Skript analysiert **Wörter** (statt Zeichen) in einer Textdatei:

1. **Eingabe:** Es liest **sampletext.txt** (im gleichen Ordner). Kommas und Punkte werden durch Leerzeichen ersetzt, dann wird nach Leerzeichen in Wörter zerlegt.
2. **Häufigkeit:** Es zählt, wie oft jedes Wort vorkommt, und sortiert die Wörter absteigend nach Häufigkeit.
3. **Entropie:** Pro Wort werden Wahrscheinlichkeit *p* und Entropie *H* = log₂(1/*p*) (in bit/Wort) berechnet, sowie die durchschnittliche Entropie (bit/Wort) und die Gesamtentropie in bit bzw. Byte.
4. **Ausgabe:** Tabelle (Wort, Anzahl, *p*, *H*) sowie die Kennzahlen und die Dateigröße von sampletext.txt. Die Konsolenausgabe wird parallel in **submissions/console_log.txt** geschrieben (für „Konsolenausgabe einfügen“ im Launcher).

Am Ende hält eine Endlosschleife die Konsole offen.
