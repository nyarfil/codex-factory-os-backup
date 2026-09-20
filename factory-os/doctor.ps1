$ErrorActionPreference = "Stop"
& "$PSScriptRoot\06-lifecycle\scripts\doctor.ps1" @args
exit $LASTEXITCODE
