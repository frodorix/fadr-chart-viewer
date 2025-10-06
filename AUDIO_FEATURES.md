# 🎵 Generador de Audio de Escalas - Nueva Funcionalidad

## ✨ Nueva Característica Agregada

Se ha añadido una **nueva funcionalidad de generación de audio** que permite crear archivos de audio WAV con escalas de acordes para práctica musical.

## 🎯 Características del Generador de Audio

### 🎼 **Escalas Soportadas**
- **Acordes mayores**: C, D, E, F, G, A, B
- **Acordes menores**: Cm, Dm, Em, Am, etc.
- **Acordes de séptima**: C7, G7, Cmaj7, Am7, etc.
- **Alteraciones**: C#, Bb, F#m, Ebmaj7, etc.

### ⚙️ **Configuración Personalizable**
- **Duración por nota**: 200ms - 2000ms (configurable)
- **Repeticiones**: 1-10 veces
- **Dirección**: Ascendente, descendente, o ambas
- **Formato de salida**: Archivo WAV de alta calidad

### 🎵 **Generación de Audio**
- **Calidad**: 44.1 kHz, 16-bit, mono
- **Envolvente**: Fade in/out automático para evitar clicks
- **Normalización**: Audio normalizado para volumen óptimo

## 🚀 Cómo Usar la Nueva Funcionalidad

### 1. **Acceder al Generador de Audio**
```
1. Ejecuta la aplicación: python -m streamlit run streamlit_app.py
2. En el menú principal, selecciona: "🎵 Generar Audio de Escalas"
```

### 2. **Configurar la Escala**
- **Nombre del acorde**: Ingresa el acorde (ej: C, Am, G7)
- **Duración por nota**: Ajusta el tiempo entre notas (recomendado: 700ms)
- **Repeticiones**: Cuántas veces reproducir la escala
- **Dirección**: Selecciona ascendente, descendente, o ambas

### 3. **Generar y Descargar**
- Haz clic en "🎵 Generar Audio de Escala"
- Escucha el preview en el navegador
- Descarga el archivo WAV para uso offline

## 📋 Ejemplos de Uso

### **Práctica básica de escalas mayores:**
```
Acorde: C
Duración: 700ms
Repeticiones: 3
Dirección: Ascendente y descendente
```

### **Estudio de acordes menores:**
```
Acorde: Am
Duración: 500ms
Repeticiones: 2
Dirección: Solo ascendente
```

### **Escalas de séptima para jazz:**
```
Acorde: Cmaj7
Duración: 800ms
Repeticiones: 1
Dirección: Ambas direcciones
```

## 🎼 Teoría Musical Implementada

### **Intervalos por tipo de acorde:**
- **Mayor/maj**: 1-2-3-4-5-6-7 (T-T-S-T-T-T-S)
- **Menor/m**: 1-2-♭3-4-5-♭6-♭7 (T-S-T-T-S-T-T)
- **Dominante/7**: 1-2-3-4-5-6-♭7
- **Mayor séptima/maj7**: 1-2-3-4-5-6-7

### **Frecuencias calculadas:**
- Basadas en el temperamento igual
- A4 = 440 Hz como referencia
- Fórmula: f = 440 × 2^((n-69)/12)

## 🔧 Dependencias Agregadas

```txt
numpy>=1.21.0  # Para procesamiento de audio
```

## 💡 Casos de Uso Educativos

### **Para estudiantes:**
- Memorizar escalas de acordes
- Entrenar el oído musical
- Practicar improvisación

### **Para profesores:**
- Crear material de audio personalizado
- Demostrar diferencias entre escalas
- Ejercicios de entrenamiento auditivo

### **Para músicos:**
- Calentar antes de tocar
- Estudiar progresiones de acordes
- Referencia rápida de escalas

## 🎯 Beneficios de la Funcionalidad

✅ **Práctica personalizada** con timing ajustable
✅ **Audio de alta calidad** para entrenamiento
✅ **Escalas teóricamente correctas**
✅ **Descarga offline** para uso sin conexión
✅ **Interface intuitiva** y fácil de usar
✅ **Múltiples tipos de acordes** soportados

## 🔄 Integración con Chart de Acordes

La nueva funcionalidad se integra perfectamente con el generador de charts:
1. **Visualiza** el chart de acordes de tu canción
2. **Practica** las escalas de los acordes individuales
3. **Combina** ambas herramientas para estudio completo

## 🎉 Resultado Final

Una herramienta completa que combina:
- **📊 Análisis visual** de progresiones de acordes
- **🎵 Entrenamiento auditivo** con escalas generadas
- **📄 Exportación** de charts y audio
- **⚙️ Configuración flexible** para todos los niveles

¡Perfecto para músicos, estudiantes y profesores de música!