# -*- coding: utf-8 -*-
"""
Bierdeckel-Quiz: Analogie Zahlensystem.
R = 30 Bierdeckel insgesamt (Bezeichnungsraum).
B = Basis = Anzahl Brauereien → n = R/B Stellen (Deckel pro Brauerei).
V = B^n = Anzahl darstellbarer Nachrichten. Theorie: Optimum bei B = e (Eulersche Zahl).
"""
import math
import os
import sys
import time

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_CONSOLE_LOG_PATH = os.path.join(_SCRIPT_DIR, "submissions", "console_log.txt")


class _Tee:
    """Schreibt gleichzeitig in Konsole und Datei."""
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
            if getattr(s, "flush", None):
                s.flush()
    def flush(self):
        for s in self.streams:
            if getattr(s, "flush", None):
                s.flush()
    def writable(self):
        return True


_log_file = None
try:
    os.makedirs(os.path.dirname(_CONSOLE_LOG_PATH), exist_ok=True)
    _log_file = open(_CONSOLE_LOG_PATH, "w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, _log_file)
except OSError:
    pass

# --- Parameter: R = 30 Bierdeckel insgesamt ---
R = 30
try:
    s = input(f"Anzahl Bierdeckel R (Bezeichnungsraum) [Standard {R}]: ").strip()
    if s:
        R = int(s)
        if R < 1 or R > 1000:
            R = 30
except (ValueError, EOFError):
    pass

print(f"\nBierdeckel-Telegraf: R = {R} Deckel (Bezeichnungsraum), B = Brauereien (Basis)")
print("n = R/B Stellen,  V = B^n = Signalvorrat,  G = log2(V) = Entscheidungsgehalt (H = G in bit)")
print("=" * 60)

# Nur B, die R teilen (damit n = R/B ganzzahlig)
candidates = [b for b in range(1, R + 1) if R % b == 0]
rows = []
best_B, best_n, best_V, best_G = 1, R, 1, 0.0

for B in candidates:
    n = R // B
    V = B ** n
    G = math.log2(V) if V > 0 else 0
    rows.append((B, n, V, G))
    if V > best_V:
        best_V = V
        best_B = B
        best_n = n
        best_G = G

def _fmt(V):
    if V < 1e12:
        return str(int(V))
    return f"{V:.4e}"

print(f"\n{'B':>4} | {'n=R/B':>6} | {'V = B^n':>14} | {'G = log2(V) [bit]':>12}")
print("-" * 42)
for B, n, V, G in rows:
    print(f"{B:>4} | {n:>6} | {_fmt(V):>14} | {G:>12.2f}")

print("\n" + "=" * 60)
print(f"Optimum: B = {best_B}  (n = {best_n} Stellen)  =>  V_max = {_fmt(best_V)},  G_max = {best_G:.2f} bit (H = G)")
print(f"Theorie: B = e ≈ {math.e:.2f} ist optimal; bei ganzzahligem B oft B = 2 oder B = 3.")

if _log_file is not None:
    try:
        sys.stdout = sys.__stdout__
        _log_file.close()
    except (OSError, NameError):
        pass

while True:
    time.sleep(1)
