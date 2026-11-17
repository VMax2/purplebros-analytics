$ErrorActionPreference = 'Stop'
$url = 'https://github.com/git-for-windows/git/releases/download/v2.56.0.windows.4/MinGit-2.56.0.4-64-bit.zip'
$destZip = Join-Path $env:TEMP 'MinGit.zip'
$targetDir = 'C:\Users\Max\AppData\Local\Programs\MinGit'

Write-Host "Scaricamento MinGit in corso..."
Invoke-WebRequest -Uri $url -OutFile $destZip -UseBasicParsing

Write-Host "Estrazione MinGit in corso..."
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}
Expand-Archive -Path $destZip -DestinationPath $targetDir -Force
Remove-Item $destZip -Force

# Aggiunge MinGit al PATH dell'utente per persistenza
$userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
$gitCmdDir = Join-Path $targetDir 'cmd'
if ($userPath -notlike "*$gitCmdDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$gitCmdDir", [EnvironmentVariableTarget]::User)
}

Write-Host "MinGit installato con successo!"
& "$gitCmdDir\git.exe" --version
