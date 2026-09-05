@echo off
title Compilador Nativo C++ (Nuitka) - OpenRGB Flowers
cd /d "%~dp0"
echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul
echo ========================================================
echo   Iniciando compilacao nativa em C++ com Nuitka...
echo ========================================================
python build_nuitka.py
echo.
echo ========================================================
echo   Concluido! Abrindo a pasta dist no Windows Explorer...
echo ========================================================
explorer.exe "%~dp0dist"
pause
