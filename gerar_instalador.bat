@echo off
title Criador de Instalador Inno Setup - OpenRGB Flowers GUI
cd /d "%~dp0"

echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM FlowersBlooming_Setup.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul

echo.
echo ========================================================
echo   CRIADOR DE INSTALADOR PROFISSIONAL (Inno Setup)
echo   OpenRGB Flowers Blooming (GUI, Icones e Sem Console)
echo ========================================================
echo   [1] Compilar Standalone com Nuitka e Gerar Instalador (Completo)
echo   [2] Gerar Instalador a partir do Standalone existente em dist/
echo.
set MODO=1
set /p MODO="Digite 1 ou 2 [Padrao: 1]: "

where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao foi encontrado no PATH do sistema.
    echo Certifique-se de que o Python esteja instalado e marcado "Add to PATH".
    pause
    exit /b 1
)

if "%MODO%"=="2" (
    echo.
    echo [INFO] Gerando instalador a partir dos binarios existentes...
    python build_installer.py --skip-nuitka
) else (
    echo.
    echo [INFO] Compilando Standalone com Nuitka e gerando instalador...
    python build_installer.py --compile-nuitka
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
