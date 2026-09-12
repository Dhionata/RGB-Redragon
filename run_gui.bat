@echo off
cd /d "%~dp0"
if exist "dist\FlowersBlooming_Portable\FlowersBlooming.exe" (
    start "" "dist\FlowersBlooming_Portable\FlowersBlooming.exe" --gui
) else if exist "dist\FlowersBlooming.exe" (
    start "" "dist\FlowersBlooming.exe" --gui
) else if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "%~dp0launcher.py" --gui
) else if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" "%~dp0launcher.py" --gui
) else (
    start "" pythonw "%~dp0launcher.py" --gui
)
exit
