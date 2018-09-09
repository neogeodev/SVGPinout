@echo off
for %%f in (svg\*.svg) do (
    echo %%~f
    "D:\Program Files\Inkscape\inkscape.exe" ^
      -z ^
      --export-background-opacity=0 ^
      --export-png="png\%%~nf.png" ^
      --file="%%~f"
)