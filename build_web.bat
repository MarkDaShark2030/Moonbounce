@echo off
setlocal

rem Build the browser version from main.py and place it in build\web\.
cd /d "%~dp0"

set "PYTHON_BIN=python"
if not "%PYTHON_BIN_OVERRIDE%"=="" set "PYTHON_BIN=%PYTHON_BIN_OVERRIDE%"

%PYTHON_BIN% -c "import pygbag" >nul 2>nul
if errorlevel 1 (
    if defined VIRTUAL_ENV (
        %PYTHON_BIN% -m pip install --upgrade pygbag
    ) else (
        if not exist ".venv\Scripts\python.exe" %PYTHON_BIN% -m venv .venv
        if errorlevel 1 exit /b 1
        set "PYTHON_BIN=.venv\Scripts\python.exe"
        %PYTHON_BIN% -m pip install --upgrade pip pygbag
    )
)
if errorlevel 1 exit /b 1

%PYTHON_BIN% -m pygbag --build --html --ume_block 0 --disable-sound-format-error --title "Moonbounce" --width 960 --height 640 .
if errorlevel 1 exit /b 1

copy /Y web_index.html build\web\index.html >nul
if errorlevel 1 exit /b 1

echo Built build\web\moonbounce.html
endlocal
