# Was macht beer_coaster.py?

Das Skript berechnet **Signalvorrat V** und **Entscheidungsgehalt G = log₂(V)** (Informationsgehalt H = G) für den **Bierdeckel-Telegrafen** (Analogie zur optischen Telegraphie):

- **R** = 30 Bierdeckel insgesamt (Bezeichnungsraum), **B** = Basis = Anzahl Brauereien, **n = R/B** = Anzahl Stellen.
- **V = B^n** = Anzahl darstellbarer Nachrichten, **G = log₂(V)** in bit (= H bei Gleichverteilung).
- Es werden nur **B** betrachtet, die **R teilen**. Tabelle: B, n, V, G; Optimum (maximaler Informationsgehalt). Theorie: **B = e** optimal; ganzzahlig oft **B = 2** oder **B = 3**.
- Konsolenausgabe parallel in **submissions/console_log.txt** (Launcher: „Konsolenausgabe einfügen“).
