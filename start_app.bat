@echo off
echo ========================================
echo    Generador de Chart de Acordes
echo ========================================
echo.
echo Elige una opcion:
echo.
echo 1. Ejecutar con Streamlit (Python) - Recomendado
echo 2. Ejecutar con Flutter (requiere instalacion)
echo 3. Instalar Flutter automaticamente
echo 4. Salir
echo.
set /p choice="Ingresa tu opcion (1-4): "

if "%choice%"=="1" (
    echo.
    echo Ejecutando aplicacion Streamlit...
    echo (Se abrira en tu navegador web)
    python -m streamlit run streamlit_app.py
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Error: Python o Streamlit no estan instalados
        echo Instala las dependencias con: pip install streamlit pandas fpdf2
        pause
    )
) else if "%choice%"=="2" (
    echo.
    echo Ejecutando aplicacion Flutter...
    call run_flutter_app.bat
) else if "%choice%"=="3" (
    echo.
    echo Instalando Flutter...
    call install_flutter.bat
) else if "%choice%"=="4" (
    echo Saliendo...
    exit /b 0
) else (
    echo.
    echo ❌ Opcion invalida. Intenta de nuevo.
    pause
    goto :eof
)

pause