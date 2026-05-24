@echo off
set PYTHON_SCRIPTS=%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts

%PYTHON_SCRIPTS%\pyinstaller ^
    --onefile ^
    --windowed ^
    --icon="C:\Users\Edison Pates\Documents\Forbidden content\AMRAAM-Chan hum.ico" ^
    --name="VolumeKnocker" ^
    --add-data="C:\Users\Edison Pates\Documents\Forbidden content\AMRAAM-Chan hum.png;." ^
    Volume_Knocker.py

if exist "dist\VolumeKnocker.exe" (
    echo.
    echo Build successful! Executable created at: %CD%\dist\VolumeKnocker.exe
    echo.
    pause
) else (
    echo.
    echo Build failed. Check for errors above.
    pause
)
