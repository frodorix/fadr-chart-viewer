# 🛠️ Instalación de Flutter para Windows

## ⬇️ Instalación Automática (Recomendado)

### Usando Git (si tienes Git instalado):
```cmd
cd C:\
git clone https://github.com/flutter/flutter.git -b stable
```

### Descarga Manual:
1. Ve a: https://docs.flutter.dev/get-started/install/windows
2. Descarga "Flutter SDK" para Windows
3. Extrae el archivo ZIP a `C:\flutter`

## 🔧 Configuración del PATH

### Opción 1: Interfaz Gráfica
1. Presiona `Win + R`, escribe `sysdm.cpl` y presiona Enter
2. Ve a la pestaña "Avanzado"
3. Haz clic en "Variables de entorno"
4. En "Variables del sistema", selecciona "Path" y haz clic en "Editar"
5. Haz clic en "Nuevo" y agrega: `C:\flutter\bin`
6. Haz clic en "Aceptar" en todas las ventanas

### Opción 2: PowerShell (como Administrador)
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\flutter\bin", "Machine")
```

## ✅ Verificación

Abre una nueva ventana de cmd y ejecuta:
```cmd
flutter --version
flutter doctor
```

## 🚀 Ejecutar la aplicación

Una vez instalado Flutter:
```cmd
run_flutter_app.bat
```

## 🔄 Alternativa: Usar Streamlit

Si prefieres no instalar Flutter, puedes usar la versión Streamlit:
```cmd
python -m streamlit run chart_chord_generator.py
```

## 📋 Requisitos del Sistema

- Windows 10 o superior (64-bit)
- Git para Windows (opcional pero recomendado)
- Visual Studio o Visual Studio Code (para desarrollo)
- Chrome (para ejecutar en web si Windows no está disponible)

## 🆘 Solución de Problemas

### Error: "flutter no se reconoce"
- Reinicia la ventana de cmd después de configurar el PATH
- Verifica que la ruta `C:\flutter\bin` exista
- Asegúrate de haber agregado el PATH correctamente

### Error al ejecutar la aplicación
- Ejecuta `flutter doctor` para ver problemas
- Acepta las licencias de Android: `flutter doctor --android-licenses`
- Prueba ejecutar en Chrome: `flutter run -d chrome`

### Problemas de permisos
- Ejecuta cmd como Administrador
- Verifica permisos de escritura en `C:\flutter`