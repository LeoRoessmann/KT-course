"""
Prüft, welche Prozesse bestimmte Ports belegen (z. B. 8081, 8082), und kann diese
optional beenden, um „hängende“ Sockets freizugeben (z. B. nach abgestürztem NiceGUI).

Verwendung (aus KT-workspace):
  python lab_suite/scripts/check_ports.py           # Ports 8081, 8082 prüfen
  python lab_suite/scripts/check_ports.py 8081    # nur 8081
  python lab_suite/scripts/check_ports.py 8081 -k # Port 8081 freigeben (Prozess beenden)

Windows: netstat + taskkill. Linux/macOS: lsof + kill.
"""
from __future__ import annotations

import argparse
import subprocess
import sys


# Typische Dev-Ports für Launcher/Labs
DEFAULT_PORTS = [8081, 8082]


def get_pids_on_port_windows(port: int) -> list[int]:
    """Ermittelt PIDs, die den Port unter Windows belegen (netstat -ano)."""
    try:
        out = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if out.returncode != 0:
        return []
    pids: set[int] = set()
    port_str = f":{port}"
    for line in out.stdout.splitlines():
        line = line.strip()
        # LISTENING oder deutsche Locale (ABHÖREN)
        if (port_str in line and
                ("LISTENING" in line or "ABH" in line or "ESTABLISHED" in line)):
            parts = line.split()
            if len(parts) >= 1 and parts[-1].isdigit():
                pids.add(int(parts[-1]))
    return sorted(pids)


def get_pids_on_port_unix(port: int) -> list[int]:
    """Ermittelt PIDs, die den Port unter Linux/macOS belegen (lsof)."""
    try:
        out = subprocess.run(
            ["lsof", "-i", f":{port}", "-t"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if out.returncode != 0:
        return []
    pids = []
    for line in out.stdout.strip().splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return sorted(set(pids))


def get_pids_on_port(port: int) -> list[int]:
    if sys.platform == "win32":
        return get_pids_on_port_windows(port)
    return get_pids_on_port_unix(port)


def get_process_name_windows(pid: int) -> str:
    """Versucht, den Prozessnamen zu einem PID unter Windows zu ermitteln."""
    try:
        out = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    if out.returncode != 0 or not out.stdout.strip():
        return ""
    # "name.exe","12345",...
    parts = out.stdout.strip().split(",")
    if parts:
        name = parts[0].strip('"')
        return name
    return ""


def kill_process_windows(pid: int) -> bool:
    try:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            capture_output=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return True
    except Exception:
        return False


def kill_process_unix(pid: int) -> bool:
    try:
        subprocess.run(["kill", "-9", str(pid)], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prüft belegte Ports (z. B. 8081) und kann Prozesse beenden, um den Port freizugeben."
    )
    parser.add_argument(
        "ports",
        nargs="*",
        type=int,
        default=DEFAULT_PORTS,
        help=f"Port(s) zum Prüfen (Standard: {DEFAULT_PORTS})",
    )
    parser.add_argument(
        "-k",
        "--kill",
        action="store_true",
        help="Prozesse, die den Port belegen, beenden (Port freigeben)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Nur PIDs ausgeben (für Skripte)",
    )
    args = parser.parse_args()

    ports = args.ports if isinstance(args.ports, list) else [args.ports]
    any_found = False
    for port in ports:
        pids = get_pids_on_port(port)
        if not pids:
            if not args.quiet:
                print(f"Port {port}: nicht belegt.")
            continue
        any_found = True
        if args.quiet:
            for pid in pids:
                print(pid)
            continue
        print(f"Port {port} wird belegt von PID(s): {pids}")
        if sys.platform == "win32":
            for pid in pids:
                name = get_process_name_windows(pid)
                if name:
                    print(f"  PID {pid}: {name}")
        if args.kill:
            for pid in pids:
                ok = kill_process_windows(pid) if sys.platform == "win32" else kill_process_unix(pid)
                if ok:
                    print(f"  PID {pid} beendet.")
                else:
                    print(f"  PID {pid} konnte nicht beendet werden (evtl. Admin-Rechte nötig).")

    if not any_found and not args.quiet and not args.kill:
        print("Keine der angegebenen Ports ist belegt.")
    sys.exit(0 if not args.kill or not any_found else 0)


if __name__ == "__main__":
    main()
