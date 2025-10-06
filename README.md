# Generador de Chart de Acordes con Streamlit

Esta aplicación genera un chart de acordes musical basado en datos CSV y permite exportarlo a PDF.

## Características

- 🎵 Interfaz web interactiva con Streamlit
- ⚙️ Configuración ajustable de BPM, compases por línea, y espaciado
- 📊 Visualización en tiempo real del chart de acordes
- 📄 Exportación a PDF
- 🎼 Formato similar a charts musicales profesionales

## Instalación y Ejecución

### Opción 1: Usando el archivo batch (Recomendado)
1. Hacer doble clic en `run_app.bat`
2. La aplicación se abrirá automáticamente en tu navegador

### Opción 2: Línea de comandos
1. Abrir cmd (no PowerShell)
2. Navegar al directorio del proyecto:
   ```
   cd "C:\Users\edwin.rojas\Downloads\[fadr.com] Midi - Me has dado libertad"
   ```
3. Instalar dependencias:
   ```
   python -m pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```
   python -m streamlit run streamlit_app.py
   ```

## Uso de la Aplicación

1. **Seleccionar archivo CSV**: La aplicación detecta automáticamente archivos .csv en el directorio
2. **Configurar parámetros** en la barra lateral:
   - **BPM**: Beats por minuto de la canción (60-200)
   - **Beats por compás**: 3, 4, 6, u 8 beats
   - **Compases por línea**: Cuántos compases mostrar por línea (2-8)
   - **Espaciado**: Caracteres por beat para ajustar el espaciado
3. **Visualizar el chart**: Se muestra en tiempo real mientras ajustas los parámetros
4. **Exportar a PDF**: Hacer clic en "Generar PDF" y descargar el archivo

## Formato del archivo CSV

El archivo CSV debe tener las siguientes columnas:
- `chord`: Nombre del acorde (ej: "G:maj", "A:min")
- `start`: Tiempo de inicio en segundos
- `end`: Tiempo de finalización en segundos

## Dependencias

- streamlit >= 1.28.0
- pandas >= 1.5.0
- fpdf2 >= 2.7.0

## Notas

- Los acordes se simplifican automáticamente (:maj se quita, :min se convierte a 'm')
- El chart incluye números de compás y líneas de separación
- La aplicación se abre automáticamente en el navegador (generalmente en http://localhost:8501)