@echo off
.\CMHVenv\Scripts\python.exe .\CMH\main.py
pause
.\miktex-portable\texmfs\install\miktex\bin\x64\pdflatex.exe -synctex=1 -quiet -interaction=nonstopmode .\CMH\Files\Procedimiento.tex -output-directory=.\CMH\Files\Build
start "" ".\CMH\Files\Build\Procedimiento.pdf" --hide
exit
