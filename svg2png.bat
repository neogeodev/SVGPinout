@echo off
for %%f in (*.svg) do (
    echo %%~f
    "D:\Program Files\Inkscape\inkscape.exe" ^
      -z ^
      --export-background-opacity=0 ^
      --export-png="%%~dpnf_pinout.png" ^
      --file="%%~f"

)