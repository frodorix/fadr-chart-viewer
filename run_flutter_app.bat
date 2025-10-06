@echo off
echo ========================================
echo    Chord Chart Generator - Flutter
echo ========================================
echo.

echo Verificando si Flutter esta instalado...
flutter --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Flutter no esta instalado o no esta en el PATH
    echo.
    echo Para instalar Flutter, sigue estos pasos:
    echo.
    echo 1. Ve a: https://docs.flutter.dev/get-started/install/windows
    echo 2. Descarga Flutter SDK para Windows
    echo 3. Extrae el archivo ZIP a C:\flutter
    echo 4. Agrega C:\flutter\bin al PATH del sistema
    echo.
    echo Alternativamente, puedes usar la aplicacion Streamlit:
    echo - Ejecuta: python -m streamlit run streamlit_app.py
    echo.
    pause
    exit /b 1
)

echo ✅ Flutter encontrado
flutter --version

echo.
echo Verificando directorio del proyecto...
if not exist "flutter_chord_chart" (
    echo ❌ Directorio flutter_chord_chart no encontrado
    echo Asegurate de estar en el directorio correcto
    pause
    exit /b 1
)

cd flutter_chord_chart

echo.
echo Instalando dependencias de Flutter...
flutter pub get

echo.
echo Verificando configuracion de Flutter...
flutter doctor --android-licenses >nul 2>&1
flutter doctor

echo.
echo Intentando ejecutar la aplicacion...
echo (Se intentara abrir en Windows, si no funciona, prueba con Chrome)

flutter run -d windows
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  No se pudo ejecutar en Windows, intentando con Chrome...
    flutter run -d chrome
)

pause