@echo off
cd /d "%~dp0"
echo Directorio actual: %CD%
echo.
echo Instalando dependencias...
python -m pip install -r requirements.txt

echo.
echo Iniciando aplicacion Streamlit...
python -m streamlit run chart_chord_generator.py

pause