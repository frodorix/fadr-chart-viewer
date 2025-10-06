@echo off
cd /d "%~dp0"
echo ========================================
echo    Generador de Chart de Acordes
echo        con Audio de Escalas
echo ========================================
echo Directorio actual: %CD%
echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Verificando instalacion...
python -c "import streamlit, pandas, numpy, fpdf; print('✅ Todas las dependencias instaladas correctamente')"

echo.
echo Iniciando aplicacion Streamlit...
echo (Se abrira automaticamente en tu navegador)
python -m streamlit run streamlit_app.py

pause