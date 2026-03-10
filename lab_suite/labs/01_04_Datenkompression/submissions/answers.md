# Fragebogen: Wort-Entropie (word_dictionary.py)

Nach dem Ausführen von `word_dictionary.py` mit eigenem Text in `sampletext.txt`:

**Konsolenausgabe einfügen:** Nutze das Merge-Symbol in der Task-Card, um die Ausgabe aus `console_log.txt` hier einzufügen. Anschließend die Ausgabe **kommentieren**.

---

**1. Konsolenausgabe**

*(Wird per „Konsolenausgabe einfügen“ unten eingefügt. Danach bitte kommentieren.)*

---

**2. Deine Kommentierung**

- Wie unterscheidet sich die Wort-Entropie von der Zeichen-Entropie (entropy1.py)?  
  *[kurz beschreiben]*
Man sieht, dass die meisten Wörter nur einmal vorkommen (Total number = 60; Number of different words = 54). Die Verteilung ist gleichmäßiger und darum ist die durchschnittliche Wort-Entropie höher als die Zeichen-Entropie.

- Was sagt die Entropie in Byte im Vergleich zur tatsächlichen Dateigröße aus?  
  *[kurz begründen]*
Size of text file (476 Bytes) ist die reale Datei auf der Festplatte. Total Entropy of 60 Words (43 Bytes) gibt den Informationsgehalt der 60 Wörter an. Wenn man die Datei perfekt komprimieren könnte wäre die Datei nur 43 Byte groß.

---

## Konsolenausgabe

```
Analyze the file:  C:\Users\leoro\Desktop\KT\KT-course\lab_suite\labs\01_04_Datenkompression\submissions\sampletext.txt
Total number of words:     60
Number of different words: 54

-------Table of words:-----------------------------------------
                       Entropie | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                              - | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                        gesagt: | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                            die | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                            ein | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                             zu | cnt=  2    p=0.033   H=4.907 bit/word   H_av=0.164 bit/word
                            ist | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                             in | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            der | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
           Informationstheorie: | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                        einfach | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
              durchschnittliche | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         Anzahl | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            von | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                 Entscheidungen | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         (Bits) | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                      benÃ¶tigt | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         werden | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                             um | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                        Zeichen | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            aus | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                          einer | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                   Zeichenmenge | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                 identifizieren | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           oder | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                      isolieren | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         anders | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           MaÃŸ | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                        welches | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           fÃ¼r | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           eine | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
              Nachrichtenquelle | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            den | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                      mittleren | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
             Informationsgehalt | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                   ausgegebener | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                    Nachrichten | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         angibt | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            Das | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
       informationstheoretische | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                   VerstÃ¤ndnis | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            des | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                      Begriffes | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           geht | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            auf | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                         Claude | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                              E | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                        Shannon | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                        zurÃ¼ck | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                            und | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                      existiert | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           seit | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           etwa | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
                           1948 | cnt=  1    p=0.017   H=5.907 bit/word   H_av=0.098 bit/word
-----------------------------------------------------------------

Average Entropy H = 5.707 bit/word
Total Entropy of 60 words H=342.413 bit (43 bytes)
Size of text file: 476 bytes
```
