@echo off
title Compilador Nativo C++ (Nuitka) - OpenRGB Flowers
cd /d "%~dp0"
echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul
echo ========================================================
echo   ESCOLHA O FORMATO DE COMPILACAO (Nuitka C++):
echo ========================================================
echo   [1] Pasta Portatil Standalone (RECOMENDADO: 0 falsos positivos / Sem Static ML)
echo   [2] Arquivo Unico .exe (Onefile compactado)
echo.
set /p MODO="Digite 1 ou 2 [Padrao: 1]: "
if "%MODO%"=="2" (
    echo Compilando modo Arquivo Unico (.exe)...
    python build_nuitka.py
    if errorlevel 1 (
        echo.
        echo [ERRO] A compilacao falhou. Verifique as mensagens de erro acima.
        pause
        exit /b 1
    )
    echo.
    echo ========================================================
    echo   Concluido! Abrindo a pasta dist no Windows Explorer...
    echo ========================================================
    explorer.exe "%~dp0dist"
) else (
    echo Compilando modo Pasta Portatil Standalone...
    python build_nuitka.py --standalone
    if errorlevel 1 (
        echo.
        echo [ERRO] A compilacao falhou. Verifique as mensagens de erro acima.
        pause
        exit /b 1
    )
    echo.
    echo ========================================================
    echo   Concluido! Abrindo a pasta portatil no Windows Explorer...
    echo ========================================================
    explorer.exe "%~dp0dist\FlowersBlooming_Portable"
)
pause
