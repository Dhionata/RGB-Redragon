@echo off
set "TARGET_DIR=%~dp0"
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $desktop = [System.Environment]::GetFolderPath('Desktop'); $s = $ws.CreateShortcut(\"$desktop\OpenRGB Flowers.lnk\"); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '-m openrgb_flowers --gui'; $s.WorkingDirectory = '%TARGET_DIR:~0,-1%'; $s.Description = 'OpenRGB Flowers Blooming & Chromatic Blend'; $s.Save(); Write-Host '[OK] Atalho criado com sucesso na sua Area de Trabalho!'"
pause
