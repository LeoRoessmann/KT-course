# Port 8082 (App-Launcher) freimachen – beendet verwaiste Prozesse.
# Ausführung: vom Repo-Root aus  .\free_port_8082.ps1

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $root "lab_suite\scripts\free_port_8082.py"
if (Test-Path $script) {
    Set-Location $root
    python $script
    Write-Host "Danach Launcher neu starten: .\start_launcher.ps1"
} else {
    Write-Host "free_port_8082.py nicht gefunden unter lab_suite/scripts/"
}
