@echo off
cd /d "%~dp0"
if exist "dist\FlowersBlooming_Portable\FlowersBlooming.exe" (
    start "" "dist\FlowersBlooming_Portable\FlowersBlooming.exe" --gui
) else if exist "dist\FlowersBlooming.exe" (
    start "" "dist\FlowersBlooming.exe" --gui
) else (
    start "" pythonw -m openrgb_flowers --gui
)
exit
