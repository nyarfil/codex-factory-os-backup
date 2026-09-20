$ErrorActionPreference = "Stop"
& "$PSScriptRoot\06-lifecycle\scripts\update.ps1" @args
exit $LASTEXITCODE
