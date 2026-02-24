##### Aufgabe: Bierdeckel-Telegraf – Maximaler Informationsgehalt (Optische Telegraphie)

**Von Flügelarmen zum Bierdeckel**

Früher gab es **optische Telegrafen**: Mit einer begrenzten Anzahl von **Stellungen** (z. B. die Arme eines Chappe-Telegrafen oder die Flügel einer Semaphore) und einer **festen Anzahl möglicher Zeichen pro Stellung** konnte man Nachrichten über weite Strecken senden. Je mehr Stellungen und Zeichen, desto mehr verschiedene Nachrichten – und damit **desto höher der Informationsgehalt** pro übertragenes „Signal“.

Unser **Bierdeckel-Telegraf** funktioniert genauso – nur mit Bierdeckeln statt Flügelarmen. Wir wollen dabei den **maximalen Informationsgehalt** pro Bierdeckel-Kombination erzielen.

---

**Größen (kurz zum Einordnen)**

- **R** = **Bezeichnungsraum** = begrenzte Anzahl Bierdeckel, die uns zur Verfügung stehen (hier **R = 30**).
- **B** = **Basis** = Anzahl **verschiedener Brauereien**, von denen wir Deckel auswählen. Nach der Wahl haben wir pro Brauerei **R/B** Deckel → das ist die **Anzahl der Stellen n** („wie viele Positionen“ unser Telegraf hat).
- **V** = **Signalvorrat** = Anzahl der darstellbaren Nachrichten (Kombinationen): **V = B^n** (n Stellen, pro Stelle eines von B Symbolen – wie beim Zahlensystem: Binär, Dezimal, Hex).
- **G** = **Entscheidungsgehalt** = wie viele binäre Entscheidungen nötig sind, um eine von V Nachrichten auszuwählen: **G = log₂(V)** (in bit). Bei gleichwahrscheinlichen Nachrichten gilt **Informationsgehalt H = G** – genau das wollen wir maximieren.

**Ablauf**

1. Wir haben eine **begrenzte Anzahl** Bierdeckel (**R = 30**).
2. Wir können uns aussuchen, **von wie vielen verschiedenen Brauereien** wir die Deckel nehmen (**Basis B**).
3. Danach bilden wir **Kombinationen mit fester Stellenanzahl** **n = R/B** (jede „Stelle“ zeigt einen von B Brauerei-Deckeln).
4. **Wann erzielen wir den maximalen Signalvorrat V und damit den höchsten Informationsgehalt H** (mit H = G) für eine Bierdeckel-Kombination?

---

**Aufgabe**

- Leitet **V = B^n** mit **n = R/B** her und **G = log₂(V)** (Entscheidungsgehalt = Informationsgehalt H bei Gleichverteilung).

- Bestimmt die **optimale Wahl von B** (nur B, die R teilen: 1, 2, 3, 5, 6, 10, 15, 30) und überprüft mit **beer_coaster.py** (Button **Starten**). Das Skript berechnet n, V und G (bzw. H) und zeigt das Maximum.

So versteht ihr **R, B, V, G und H** am Beispiel unseres Bierdeckel-Telegrafen – ganz im Geiste der optischen Telegraphie, nur eben mit Bierdeckeln.
