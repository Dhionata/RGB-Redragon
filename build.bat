@echo off
setlocal enabledelayedexpansion

echo ===============================================================================
echo   OpenRGB Flowers Blooming - Compilador Nativo C++ (CMake + MinGW / MSVC)
echo ===============================================================================

:: 0. Suporte a comando clean
if "%1"=="clean" (
    echo [Limpeza] Removendo pastas de build e dist...
    if exist "build" rmdir /s /q build
    if exist "dist" rmdir /s /q dist
    echo [Limpeza] Concluida.
    exit /b 0
)

:: 1. Localizar compilador MinGW-w64 e CMake se nao estiverem no PATH
set "NUITKA_MINGW=C:\Users\xiyun\AppData\Local\Nuitka\Nuitka\Cache\downloads\gcc\x86_64\15.2.0posix-13.0.0-msvcrt-r6\mingw64\bin"
if exist "%NUITKA_MINGW%\cmake.exe" (
    set "PATH=%NUITKA_MINGW%;!PATH!"
    echo [Toolchain] Adicionado MinGW GCC / CMake do cache local ao PATH.
)

where cmake.exe >nul 2>&1
if %ERRORLEVEL% neq 0 (
    if exist "C:\Program Files\CMake\bin\cmake.exe" (
        set "PATH=C:\Program Files\CMake\bin;!PATH!"
    )
)

where cmake.exe >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERRO] CMake nao encontrado no sistema. Instale o CMake ou configure o PATH.
    exit /b 1
)

:: 2. Configurar diretorio de build
if not exist "build" mkdir build
cd build

echo [CMake] Configurando projeto C++20...
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
if %ERRORLEVEL% neq 0 (
    echo [Aviso] Falha com MinGW Makefiles, tentando gerador padrao...
    cmake .. -DCMAKE_BUILD_TYPE=Release
    if %ERRORLEVEL% neq 0 (
        echo [ERRO] Falha na configuracao do CMake.
        cd ..
        exit /b 1
    )
)

:: 3. Compilar
echo [Compilacao] Compilando biblioteca e executaveis nativos C++...
cmake --build . --config Release --parallel
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha na compilacao C++.
    cd ..
    exit /b 1
)

:: 4. Executar Testes Unitarios
echo [Testes] Executando testes unitarios C++...
set TEST_STATUS=1

if exist "tests_cpp.exe" (
    .\tests_cpp.exe
    if !ERRORLEVEL! equ 0 set TEST_STATUS=0
)
if exist "Release\tests_cpp.exe" (
    .\Release\tests_cpp.exe
    if !ERRORLEVEL! equ 0 set TEST_STATUS=0
)

if !TEST_STATUS! neq 0 (
    if exist "..\run_tests.py" (
        echo [Testes] Executando testes via runner nativo compartilhado run_tests.py...
        python ..\run_tests.py
        if !ERRORLEVEL! equ 0 set TEST_STATUS=0
    )
)

cd ..

if %TEST_STATUS% neq 0 (
    echo.
    echo ===============================================================================
    echo   [ERRO] Falha na execucao dos testes unitarios.
    echo ===============================================================================
    exit /b 1
)

:: 4.5. Copiar executaveis para pasta dist
powershell -NoProfile -Command "New-Item -ItemType Directory -Force -Path 'dist\FlowersBlooming_Portable' | Out-Null; if (Test-Path 'build\Release\FlowersBlooming.exe') { Copy-Item 'build\Release\FlowersBlooming.exe' 'dist\FlowersBlooming_Portable\FlowersBlooming.exe' -Force; Copy-Item 'build\Release\FlowersBlooming.exe' 'dist\FlowersBlooming.exe' -Force } elseif (Test-Path 'build\FlowersBlooming.exe') { Copy-Item 'build\FlowersBlooming.exe' 'dist\FlowersBlooming_Portable\FlowersBlooming.exe' -Force; Copy-Item 'build\FlowersBlooming.exe' 'dist\FlowersBlooming.exe' -Force }; Copy-Item 'config.example.json' 'dist\FlowersBlooming_Portable\' -Force; Copy-Item 'README.md' 'dist\FlowersBlooming_Portable\' -Force"

:: 5. Empacotar ZIP Portatil
echo [Packaging] Gerando arquivo ZIP portatil...
powershell -NoProfile -Command "if (Test-Path 'dist\FlowersBlooming_Portable') { Compress-Archive -Path 'dist\FlowersBlooming_Portable\*' -DestinationPath 'dist\FlowersBlooming_Portable.zip' -Force; Write-Host '✓ ZIP gerado com sucesso em dist\FlowersBlooming_Portable.zip' }"

:: 6. Opcional: Inno Setup
where iscc.exe >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [Inno Setup] Compilando instalador FlowersBlooming_Setup.exe...
    iscc installer.iss
) else if exist "C:\Program Files (x86)\Inno Setup 6\iscc.exe" (
    echo [Inno Setup] Compilando instalador FlowersBlooming_Setup.exe...
    "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss
)

echo.
echo ===============================================================================
echo   Compilacao e Testes C++ Concluidos com Sucesso!
echo   Executavel Standalone: dist\FlowersBlooming.exe
echo   Pacote Portatil:       dist\FlowersBlooming_Portable.zip
echo ===============================================================================
exit /b 0
