@echo off
title Compilador Nativo C++ - OpenRGB Flowers
cd /d "%~dp0"
echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul
echo ========================================================
echo   ESCOLHA O FORMATO DE COMPILACAO:
echo ========================================================
echo   [1] C++20 Nativo Puro (CMake + MinGW/MSVC) [RECOMENDADO - 1.45 MB, 0 Falsos Positivos]
echo   [2] Python / Nuitka Standalone (Legado)
echo.
set /p MODO="Digite 1 ou 2 [Padrao: 1]: "
if "%MODO%"=="2" (
    echo Compilando modo Legado Nuitka C++...
    python build_nuitka.py --standalone
    if errorlevel 1 (
        echo.
        echo [ERRO] A compilacao falhou. Verifique as mensagens de erro acima.
        pause
        exit /b 1
    )
) else (
    echo Compilando via CMake / C++20 Nativo (build.bat)...
    call build.bat
    if errorlevel 1 (
        echo.
        echo [ERRO] A compilacao falhou. Verifique as mensagens de erro acima.
        pause
        exit /b 1
    )
)
pause
