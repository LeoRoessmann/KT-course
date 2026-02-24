# Was macht entropy1.py?

Das Skript liest die Datei **sampletext.txt** (im gleichen Ordner), zählt **wie oft jedes Zeichen** vorkommt und berechnet daraus die **Entropie** (Shannon, Informationstheorie):

- **Wahrscheinlichkeit *p* pro Zeichen** = Häufigkeit / Gesamtzeichenzahl  
- **Entropie pro Zeichen** *H* = log₂(1/*p*) (in bit)  
- **Durchschnittliche Entropie** (bit/Zeichen) und **Gesamtentropie** (bit für den ganzen Text)

Es gibt eine Tabelle (Zeichen, Anzahl, *p*, *H*) und die beiden Kennzahlen. Die Konsolenausgabe wird parallel in **submissions/console_log.txt** geschrieben (für „Konsolenausgabe einfügen“ im Launcher). Am Ende bleibt die Konsole mit einer Endlosschleife offen.
