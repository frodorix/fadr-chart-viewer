# 🎵 Chord Chart Generator - Flutter App

Una aplicación Flutter que genera charts de acordes musicales a partir de archivos CSV, con preview en tiempo real y exportación a PDF.

## ✨ Características

- 📱 **Interfaz moderna** con Flutter
- 📂 **Carga de archivos CSV** desde el dispositivo
- ⚙️ **Configuración ajustable** en tiempo real:
  - BPM (Beats por minuto): 60-200
  - Beats por compás: 3, 4, 6, 8
  - Compases por línea: 2-8
  - Espaciado entre acordes: 4-12
- 👁️ **Preview en tiempo real** del chart
- 📄 **Exportación a PDF** y compartir
- 🖨️ **Vista previa e impresión** directa
- 📊 **Estadísticas** de la canción

## 🚀 Instalación

### Prerrequisitos
- Flutter SDK (versión 3.0.0 o superior)
- Dart SDK
- Un editor como VS Code o Android Studio

### Pasos de instalación

1. **Clonar o descargar** el proyecto
2. **Navegar** al directorio del proyecto:
   ```bash
   cd flutter_chord_chart
   ```
3. **Instalar dependencias**:
   ```bash
   flutter pub get
   ```
4. **Ejecutar la aplicación**:
   ```bash
   flutter run
   ```

## 📋 Formato del archivo CSV

El archivo CSV debe tener las siguientes columnas (con encabezados):

```csv
chord,start,end
G:maj,0.650158726,2.972154176
G:min,3.018594085,3.947392265
A:min,6.315827624,6.919546441
```

Donde:
- **chord**: Nombre del acorde (ej: "G:maj", "A:min", "C:maj")
- **start**: Tiempo de inicio en segundos
- **end**: Tiempo de finalización en segundos

## 🎯 Uso de la aplicación

### 1. Cargar datos
- Haz clic en **"Cargar CSV"** para seleccionar tu archivo
- La aplicación mostrará automáticamente estadísticas del archivo

### 2. Configurar parámetros
- **BPM**: Ajusta los beats por minuto de la canción
- **Beats por compás**: Selecciona el tipo de compás (3/4, 4/4, 6/8, etc.)
- **Compases por línea**: Cuántos compases mostrar por línea
- **Espaciado**: Ajusta el espaciado entre acordes

### 3. Preview
- El chart se actualiza **automáticamente** mientras ajustas los parámetros
- Puedes ver cómo se distribuyen los acordes en tiempo real

### 4. Exportar
- **Vista Previa/Imprimir**: Abre el diálogo de impresión del sistema
- **Exportar PDF**: Genera un PDF y lo comparte usando las apps del dispositivo

## 🏗️ Estructura del proyecto

```
flutter_chord_chart/
├── lib/
│   ├── main.dart                 # Punto de entrada
│   ├── chord_chart_app.dart      # Pantalla principal
│   ├── models/
│   │   └── chord_data.dart       # Modelo de datos de acordes
│   ├── services/
│   │   ├── csv_service.dart      # Servicio para cargar CSV
│   │   └── pdf_service.dart      # Servicio para generar PDF
│   └── widgets/
│       └── chord_chart_widget.dart # Widget personalizado del chart
├── pubspec.yaml                  # Dependencias
└── README.md                     # Este archivo
```

## 📦 Dependencias principales

- **csv**: Para leer archivos CSV
- **pdf**: Para generar documentos PDF
- **printing**: Para imprimir y vista previa
- **file_picker**: Para seleccionar archivos
- **path_provider**: Para acceso al sistema de archivos
- **share_plus**: Para compartir archivos

## 🎨 Características de diseño

- **Diseño responsivo** que se adapta a diferentes tamaños de pantalla
- **Panel de control** en la izquierda con todos los controles
- **Área de preview** en la derecha con scroll
- **Indicadores visuales** de carga y estado
- **Colores y iconos** intuitivos

## 🔧 Personalización

### Modificar estilos del chart
Edita `chord_chart_widget.dart` para cambiar:
- Colores de líneas y texto
- Tamaños de fuente
- Espaciado entre elementos
- Formato de acordes

### Agregar nuevos formatos de exportación
Extiende `pdf_service.dart` para agregar:
- Diferentes formatos de página
- Estilos de chart personalizados
- Metadatos adicionales

## 🚨 Solución de problemas

### Error al cargar CSV
- Verifica que el archivo tenga el formato correcto
- Asegúrate de que tenga encabezados: `chord,start,end`
- Los valores de tiempo deben ser números válidos

### Error al exportar PDF
- Verifica que tengas permisos de escritura
- Asegúrate de tener espacio suficiente en el dispositivo

### Preview no se actualiza
- Verifica que hayas cargado un archivo CSV válido
- Reinicia la aplicación si persiste el problema

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Si tienes preguntas o problemas, por favor abre un issue en el repositorio del proyecto.