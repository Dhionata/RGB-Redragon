@echo off
title Compilador Standalone (Nuitka) - OpenRGB Flowers GUI
cd /d "%~dp0"
echo ========================================================
echo   Encerrando instancias ativas do executavel (se houver)...
echo ========================================================
taskkill /F /IM FlowersBlooming.exe /IM RedragonFlowers.exe /IM OpenRGBFlowers.exe /IM RedragonRGB.exe 2>nul
echo ========================================================
echo   ESCOLHA O FORMATO DE COMPILACAO:
echo ========================================================
echo   [1] Pasta Portatil Standalone [RECOMENDADO: Sem CMD / 0 Falsos Positivos]
echo   [2] Arquivo Unico .exe [Onefile]
echo.
set MODO=1
set /p MODO="Digite 1 ou 2 [Padrao: 1]: "

if "%MODO%"=="2" goto :BUILD_ONEFILE
goto :BUILD_STANDALONE

:BUILD_ONEFILE
echo Compilando modo Arquivo Unico [.exe] sem janela de console...
python build_nuitka.py --console-mode=disable
if errorlevel 1 goto :BUILD_ERROR
echo.
echo ========================================================
echo   Concluido! Abrindo a pasta dist no Windows Explorer...
echo ========================================================
explorer.exe "%~dp0dist"
goto :END

:BUILD_STANDALONE
echo Compilando modo Pasta Portatil Standalone com GUI e Icone...
python build_nuitka.py --standalone --console-mode=disable
if errorlevel 1 goto :BUILD_ERROR
echo.
echo ========================================================
echo   Concluido! Abrindo a pasta portatil no Windows Explorer...
echo ========================================================
explorer.exe "%~dp0dist\FlowersBlooming_Portable"
goto :END

:BUILD_ERROR
echo.
echo [ERRO] A compilacao falhou. Verifique as mensagens de erro acima.
pause
exit /b 1

:END
pause
