$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PhaseDir = Split-Path -Parent $ScriptDir
Push-Location $PhaseDir
try {
    if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 -m factory_lifecycle.cli uninstall @args; exit $LASTEXITCODE }
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3.11+ is required." }
    & python -m factory_lifecycle.cli uninstall @args
    exit $LASTEXITCODE
} finally { Pop-Location }
