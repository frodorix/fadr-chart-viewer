# 📦 Información de Dependencias

## 🔧 Dependencias Requeridas

### **Streamlit >= 1.43.0**
- **Propósito**: Framework web para crear la interfaz de usuario
- **Características usadas**: 
  - Widgets interactivos (sliders, selectores, botones)
  - Carga de archivos
  - Reproducción de audio
  - Descarga de archivos
- **Tamaño aproximado**: ~15 MB

### **Pandas >= 2.2.0**
- **Propósito**: Manipulación y análisis de datos CSV
- **Características usadas**:
  - Lectura de archivos CSV
  - DataFrames para preview de datos
  - Procesamiento de datos tabulares
- **Tamaño aproximado**: ~30 MB

### **fpdf2 >= 2.8.0**
- **Propósito**: Generación de documentos PDF
- **Características usadas**:
  - Creación de PDFs con charts de acordes
  - Formato de texto monoespaciado
  - Control de fuentes y layout
- **Tamaño aproximado**: ~2 MB

### **NumPy >= 1.26.0**
- **Propósito**: Procesamiento numérico y generación de audio
- **Características usadas**:
  - Generación de ondas senoidales
  - Procesamiento de arrays de audio
  - Cálculos matemáticos para frecuencias
- **Tamaño aproximado**: ~20 MB

## 🎯 Dependencias Opcionales

### **SciPy >= 1.11.0** (Opcional)
- **Propósito**: Mejora el procesamiento de señales de audio
- **Beneficios**: Algoritmos más avanzados para audio
- **Instalación**: `pip install scipy`

## 📋 Librerías de Python Estándar (Incluidas)

Las siguientes librerías son parte de Python y NO necesitan instalación:
- `base64` - Codificación para descarga de archivos
- `io` - Manejo de streams de datos
- `os` - Operaciones del sistema operativo
- `csv` - Procesamiento de archivos CSV
- `wave` - Manipulación de archivos de audio WAV
- `struct` - Empaquetado de datos binarios
- `math` - Funciones matemáticas

## ⚡ Instalación Rápida

### Opción 1: Usando requirements.txt
```bash
pip install -r requirements.txt
```

### Opción 2: Instalación manual
```bash
pip install streamlit pandas fpdf2 numpy
```

### Opción 3: Instalación mínima
```bash
pip install -r requirements-minimal.txt
```

## 🔍 Verificación de Instalación

Para verificar que todas las dependencias están correctamente instaladas:

```python
# Ejecutar en Python o terminal
python -c "import streamlit, pandas, numpy, fpdf; print('✅ Todo listo!')"
```

## 📊 Espacio en Disco

**Espacio total aproximado requerido**: ~70 MB
- Streamlit: ~15 MB
- Pandas: ~30 MB  
- NumPy: ~20 MB
- fpdf2: ~2 MB
- Dependencias secundarias: ~3 MB

## 🐛 Solución de Problemas

### Error al instalar NumPy
```bash
pip install --upgrade pip setuptools wheel
pip install numpy
```

### Error al instalar Pandas
```bash
pip install --no-deps pandas
pip install pytz python-dateutil
```

### Error de permisos
```bash
pip install --user -r requirements.txt
```

### Entorno virtual (Recomendado)
```bash
python -m venv chord_env
chord_env\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🔄 Actualización de Dependencias

Para mantener las dependencias actualizadas:
```bash
pip install --upgrade -r requirements.txt
```

## 💡 Notas de Compatibilidad

- **Python**: Requiere Python 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Navegador**: Chrome, Firefox, Safari, Edge (para Streamlit)
- **RAM mínima**: 4 GB recomendado
- **Espacio libre**: 100 MB mínimo