"""
Port-Prüfung und Freigabe für den App-Launcher (verwaiste Prozesse auf 8081/8082).
Wird von der Launcher-UI und optional vom Standalone-Skript lab_suite/scripts/check_ports.py genutzt.
"""
from __future__ import annotations

import subprocess
import sys

# Ports, die Labs/Launcher typisch nutzen
LAB_PORTS = [8081, 8082]


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
        if port_str in line and ("LISTENING" in line or "ABH" in line or "ESTABLISHED" in line):
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
    pids = [int(line.strip()) for line in out.stdout.strip().splitlines() if line.strip().isdigit()]
    return sorted(set(pids))


def get_pids_on_port(port: int) -> list[int]:
    if sys.platform == "win32":
        return get_pids_on_port_windows(port)
    return get_pids_on_port_unix(port)


def get_process_name_windows(pid: int) -> str:
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
    parts = out.stdout.strip().split(",")
    return parts[0].strip('"') if parts else ""


def kill_process(pid: int) -> bool:
    if sys.platform == "win32":
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
    try:
        subprocess.run(["kill", "-9", str(pid)], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def get_process_name(pid: int) -> str:
    if sys.platform == "win32":
        return get_process_name_windows(pid)
    return ""
