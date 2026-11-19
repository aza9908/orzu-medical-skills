# Установка навыков для группы Orzu Medical (Windows). Запуск: powershell -ExecutionPolicy Bypass -File install.ps1
$src = Join-Path $PSScriptRoot "skills"
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path (Join-Path $src "*") -Destination $dest -Recurse -Force
Write-Host ""
Write-Host "Готово. Установлены навыки: $((Get-ChildItem $src -Directory).Name -join ', ')"
Write-Host "Перезапустите Claude Code и наберите /airl-dwh"
