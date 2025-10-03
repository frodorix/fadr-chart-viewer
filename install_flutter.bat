@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo   Instalador Automatico de Flutter
echo ========================================
echo.

:: Verificar si Flutter ya esta instalado
flutter --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flutter ya esta instalado
    flutter --version
    echo.
    echo Ejecutando la aplicacion...
    call run_flutter_app.bat
    exit /b 0
)

echo Flutter no esta instalado. Procediendo con la instalacion...
echo.

:: Crear directorio de instalacion
if not exist "C:\flutter" (
    echo Creando directorio C:\flutter...
    mkdir "C:\flutter" 2>nul
    if !errorlevel! neq 0 (
        echo ❌ Error: No se pudo crear el directorio C:\flutter
        echo Ejecuta este script como Administrador
        pause
        exit /b 1
    )
)

:: Verificar si Git esta disponible
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Git encontrado, descargando Flutter...
    cd /d C:\
    git clone https://github.com/flutter/flutter.git -b stable
    if !errorlevel! neq 0 (
        echo ❌ Error al descargar Flutter con Git
        goto manual_download
    )
) else (
    goto manual_download
)

goto configure_path

:manual_download
echo.
echo Git no esta disponible. Descarga manual requerida:
echo.
echo 1. Ve a: https://docs.flutter.dev/get-started/install/windows
echo 2. Descarga el Flutter SDK
echo 3. Extrae el archivo ZIP a C:\flutter
echo 4. Ejecuta este script nuevamente
echo.
pause
exit /b 1

:configure_path
echo.
echo Configurando PATH...

:: Verificar si C:\flutter\bin ya esta en PATH
echo %PATH% | findstr /i "C:\flutter\bin" >nul
if %errorlevel% equ 0 (
    echo ✅ PATH ya configurado
    goto verify_installation
)

:: Agregar al PATH del usuario
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%B"
if defined UserPath (
    reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "%UserPath%;C:\flutter\bin" /f >nul
) else (
    reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "C:\flutter\bin" /f >nul
)

echo ✅ PATH configurado

:verify_installation
echo.
echo Verificando instalacion...

:: Actualizar PATH en la sesion actual
set "PATH=%PATH%;C:\flutter\bin"

:: Verificar Flutter
flutter --version
if %errorlevel% neq 0 (
    echo ❌ Error: Flutter no se pudo ejecutar
    echo Reinicia el sistema y ejecuta nuevamente
    pause
    exit /b 1
)

echo.
echo ✅ Flutter instalado exitosamente!
echo.

echo Ejecutando flutter doctor...
flutter doctor

echo.
echo ¿Deseas ejecutar la aplicacion ahora? (s/n)
set /p choice="> "

if /i "%choice%"=="s" (
    echo.
    echo Ejecutando aplicacion...
    call run_flutter_app.bat
) else (
    echo.
    echo Para ejecutar la aplicacion mas tarde, usa:
    echo run_flutter_app.bat
)

pause