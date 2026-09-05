@echo off
title Compilador de Executavel OpenRGB Flowers
cd /d "%~dp0"
echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul
echo ========================================================
echo   Iniciando geracao do executavel...
echo ========================================================
python build_exe.py
echo.
echo ========================================================
echo   Concluido! Abrindo a pasta dist no Windows Explorer...
echo ========================================================
explorer.exe "%~dp0dist"
pause
