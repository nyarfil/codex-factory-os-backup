$ErrorActionPreference = "Stop"
$PhaseDir = Join-Path $PSScriptRoot "05-governor"
Push-Location $PhaseDir
try {
  if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 -m factory_governor.cli @args; exit $LASTEXITCODE }
  if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3.11+ is recommended." }
  & python -m factory_governor.cli @args
  exit $LASTEXITCODE
} finally { Pop-Location }
