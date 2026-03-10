# Fragebogen: Entropie-Analyse (entropy1.py)

Nach dem Ausführen von `entropy1.py` mit eigenem Text in `sampletext.txt`:

**Konsolenausgabe einfügen:** Nutze das Merge-Symbol in der Task-Card, um die Ausgabe aus `console_log.txt` hier einzufügen. Anschließend die Ausgabe **kommentieren**.

---

**1. Konsolenausgabe**

*(Wird per „Konsolenausgabe einfügen“ unten eingefügt. Danach bitte kommentieren.)*

---

**2. Deine Kommentierung:**

- Was fällt dir bei der Entropie deines Textes auf?  
  *[z. B. Vergleich mit anderen Texten, Zeichenverteilung, Redundanz]*

Mein Kommentar:
Interessant ist, dass in meinem Text der häufigste Buchstabe das "e" ist. Als Häufigstes Zeichen hat es auch den geringsten Informationsgehalt (H), da häufig auftretende Zeichen weniger überraschend sind.

Der durchschnittliche Informationsgehalt des Texts liegt bei 4.537 bit/char.

---

## Konsolenausgabe

```
Analyze the file:  C:\Users\leoro\Desktop\KT\KT-course\lab_suite\labs\01_02_Informationstheorie\submissions\sampletext.txt

-----File Contents:---------------------------------------------------
Entropie ist in der Informationstheorie:



- einfach gesagt: die durchschnittliche Anzahl von Entscheidungen (Bits), die benÃ¶tigt werden, um ein Zeichen aus einer Zeichenmenge zu identifizieren oder zu isolieren,

- anders gesagt: ein MaÃŸ, welches fÃ¼r eine Nachrichtenquelle den mittleren Informationsgehalt ausgegebener Nachrichten angibt



Das informationstheoretische VerstÃ¤ndnis des Begriffes Entropie geht auf Claude E. Shannon zurÃ¼ck und existiert seit etwa 1948.

Number of characters: 472
Character Dictionary: {'E': 4, 'n': 41, 't': 30, 'r': 24, 'o': 14, 'p': 2, 'i': 39, 'e': 62, ' ': 56, 's': 22, 'd': 14, 'I': 2, 'f': 9, 'm': 6, 'a': 20, 'h': 19, ':': 3, '\n': 6, '-': 2, 'c': 14, 'g': 13, 'u': 12, 'l': 9, 'A': 1, 'z': 5, 'v': 1, '(': 1, 'B': 2, ')': 1, ',': 4, 'b': 3, 'Ã': 5, '¶': 1, 'w': 3, 'Z': 2, 'M': 1, 'Ÿ': 1, '¼': 2, 'N': 2, 'q': 1, 'D': 1, 'V': 1, '¤': 1, 'C': 1, '.': 2, 'S': 1, 'k': 1, 'x': 1, '1': 1, '9': 1, '4': 1, '8': 1}

-------Table of characters:----------------
 e     | cnt= 62    p=0.131   H=2.928 bit/char  H_av=0.385 bit/char
       | cnt= 56    p=0.119   H=3.075 bit/char  H_av=0.365 bit/char
 n     | cnt= 41    p=0.087   H=3.525 bit/char  H_av=0.306 bit/char
 i     | cnt= 39    p=0.083   H=3.597 bit/char  H_av=0.297 bit/char
 t     | cnt= 30    p=0.064   H=3.976 bit/char  H_av=0.253 bit/char
 r     | cnt= 24    p=0.051   H=4.298 bit/char  H_av=0.219 bit/char
 s     | cnt= 22    p=0.047   H=4.423 bit/char  H_av=0.206 bit/char
 a     | cnt= 20    p=0.042   H=4.561 bit/char  H_av=0.193 bit/char
 h     | cnt= 19    p=0.040   H=4.635 bit/char  H_av=0.187 bit/char
 o     | cnt= 14    p=0.030   H=5.075 bit/char  H_av=0.151 bit/char
 d     | cnt= 14    p=0.030   H=5.075 bit/char  H_av=0.151 bit/char
 c     | cnt= 14    p=0.030   H=5.075 bit/char  H_av=0.151 bit/char
 g     | cnt= 13    p=0.028   H=5.182 bit/char  H_av=0.143 bit/char
 u     | cnt= 12    p=0.025   H=5.298 bit/char  H_av=0.135 bit/char
 f     | cnt=  9    p=0.019   H=5.713 bit/char  H_av=0.109 bit/char
 l     | cnt=  9    p=0.019   H=5.713 bit/char  H_av=0.109 bit/char
 m     | cnt=  6    p=0.013   H=6.298 bit/char  H_av=0.080 bit/char
 b'\n' | cnt=  6    p=0.013   H=6.298 bit/char  H_av=0.080 bit/char
 z     | cnt=  5    p=0.011   H=6.561 bit/char  H_av=0.069 bit/char
 Ã     | cnt=  5    p=0.011   H=6.561 bit/char  H_av=0.069 bit/char
 E     | cnt=  4    p=0.008   H=6.883 bit/char  H_av=0.058 bit/char
 ,     | cnt=  4    p=0.008   H=6.883 bit/char  H_av=0.058 bit/char
 :     | cnt=  3    p=0.006   H=7.298 bit/char  H_av=0.046 bit/char
 b     | cnt=  3    p=0.006   H=7.298 bit/char  H_av=0.046 bit/char
 w     | cnt=  3    p=0.006   H=7.298 bit/char  H_av=0.046 bit/char
 p     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 I     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 -     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 B     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 Z     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 ¼     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 N     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 .     | cnt=  2    p=0.004   H=7.883 bit/char  H_av=0.033 bit/char
 A     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 v     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 (     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 )     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 ¶     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 M     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 Ÿ     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 q     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 D     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 V     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 ¤     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 C     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 S     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 k     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 x     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 1     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 9     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 4     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
 8     | cnt=  1    p=0.002   H=8.883 bit/char  H_av=0.019 bit/char
-------------------------------------------

Average Entropy H = 4.537 bit/char
Total Entropy of 472 characters H=2141.35 bit = 268.00 byte
```
