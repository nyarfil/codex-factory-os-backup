$ErrorActionPreference = "Stop"
& "$PSScriptRoot\06-lifecycle\scripts\uninstall.ps1" @args
exit $LASTEXITCODE
