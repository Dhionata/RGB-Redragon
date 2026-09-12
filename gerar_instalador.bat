@echo off
title Criador de Instalador Inno Setup - OpenRGB Flowers
cd /d "%~dp0"

echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM FlowersBlooming_Setup.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul

echo.
echo ========================================================
echo   CRIADOR DE INSTALADOR PROFISSIONAL (Inno Setup)
echo   OpenRGB Flowers Blooming
echo ========================================================
echo   [1] Compilar C++20 Nativo (CMake) e Gerar Instalador Inno Setup [RECOMENDADO]
echo   [2] Gerar Instalador a partir do Standalone existente em dist/
echo   [3] Compilar via Python/Nuitka Legado e Gerar Instalador
echo.
set MODO=1
set /p MODO="Digite 1, 2 ou 3 [Padrao: 1]: "

if "%MODO%"=="2" (
    echo.
    echo [INFO] Gerando instalador a partir dos binarios existentes...
    where iscc.exe >nul 2>&1
    if errorlevel 1 (
        if exist "C:\Program Files (x86)\Inno Setup 6\iscc.exe" (
            "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss
        ) else (
            python build_installer.py --skip-nuitka
        )
    ) else (
        iscc.exe installer.iss
    )
) else if "%MODO%"=="3" (
    echo.
    echo [INFO] Compilando Standalone com Python/Nuitka Legado e gerando instalador...
    python build_installer.py --compile-nuitka
) else (
    echo.
    echo [INFO] Compilando C++20 Nativo com CMake e gerando instalador...
    call build.bat
)

if errorlevel 1 (
    echo.
    echo ========================================================
    echo   [ERRO] O processo falhou. Verifique as mensagens acima.
    echo ========================================================
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   [SUCESSO] Instalador gerado com sucesso!
echo   Abrindo a pasta dist no Windows Explorer...
echo ========================================================
explorer.exe "%~dp0dist"
pause
