# Fragebogen: Huffman-Codierung (huffman.py)

Nach dem Ausführen des Skripts und **Einfügen der Konsolenausgabe** (Merge-Symbol in der Task-Card):

---

**1. Konsolenausgabe**

*(Wird per „Konsolenausgabe einfügen“ unten eingefügt. Danach bitte kommentieren.)*

---

**2. Deine Kommentierung**

- Was zeigen die ausgegebenen Huffman-Codes?  
  *[kurz beschreiben]*
Die Huffman-Codes zeigen die Häufigkeit eines Zeichens. Der Buchstabe "B" kam in meinem String am häufigsten vor und bekam daher den kürzesten Code.

- Warum haben häufigere Zeichen kürzere Codewörter?  
  *[kurz begründen]*
Häufigere Zeichen erhalten kürzere Codes, da dadurch die Länge der gesamten Nachricht reduziert wird.

---

## Konsolenausgabe

```
Enter the string to compute Huffman Code Tree: ---------------------------------------------------------
Dictionary of Characters with char frequency:       {'A': 4, 'D': 4, 'B': 5}
Dictionary converted into a list:                   dict_items([('A', 4), ('D', 4), ('B', 5)])
List of characters sorted to descending frequency:  [('B', 5), ('A', 4), ('D', 4)]
Huffman Code Dictionary:                            {'B': '0', 'D': '10', 'A': '11'}

 Char | Huffman code 
----------------------
 'B'  |           0
 'A'  |          11
 'D'  |          10
```
