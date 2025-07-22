@echo off
REM Windows batch script for easy config generation
REM Usage: generate_config.bat your_quantity_data.json

if "%1"=="" (
    echo Usage: generate_config.bat your_quantity_data.json
    echo.
    echo Example: generate_config.bat quantity_mode_analysis.json
    echo This will generate a ready-to-use configuration file.
    pause
    exit /b 1
)

echo 🚀 Generating configuration from %1...
python generate_config_ascii.py %1 %2 %3 %4 %5

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Success! Your configuration is ready to use.
) else (
    echo.
    echo ❌ Generation failed. Check the error messages above.
)

pause