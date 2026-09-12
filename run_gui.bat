@echo off
cd /d "%~dp0"
if exist "dist\FlowersBlooming.exe" (
    start "" "dist\FlowersBlooming.exe" --tray
) else if exist "build\FlowersBlooming.exe" (
    start "" "build\FlowersBlooming.exe" --tray
) else (
    echo [FlowersBlooming] Binario nativo C++ nao encontrado. Compilando via build.bat...
    call build.bat
    if exist "dist\FlowersBlooming.exe" (
        start "" "dist\FlowersBlooming.exe" --tray
    )
)
