import streamlit as st
import pandas as pd
import csv
from fpdf import FPDF
import base64
import io
import os

def load_chord_data(csv_file):
    """Cargar datos de acordes desde archivo CSV"""
    chords = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                chords.append({
                    'chord': row['chord'],
                    'start': float(row['start']),
                    'end': float(row['end'])
                })
    except FileNotFoundError:
        st.error(f"Archivo {csv_file} no encontrado")
        return []
    return chords

def load_chord_data_from_uploaded_file(uploaded_file):
    """Cargar datos de acordes desde archivo CSV subido"""
    chords = []
    try:
        # Leer el contenido del archivo subido
        content = uploaded_file.read().decode('utf-8')
        
        # Verificar que el archivo no esté vacío
        if not content.strip():
            st.error("El archivo está vacío")
            return []
        
        reader = csv.DictReader(io.StringIO(content))
        
        # Verificar que tiene las columnas necesarias
        required_columns = {'chord', 'start', 'end'}
        if not required_columns.issubset(reader.fieldnames):
            st.error(f"El archivo debe tener las columnas: {', '.join(required_columns)}")
            st.error(f"Columnas encontradas: {', '.join(reader.fieldnames) if reader.fieldnames else 'Ninguna'}")
            return []
        
        # Procesar filas
        invalid_rows = []
        for i, row in enumerate(reader):
            try:
                chord_data = {
                    'chord': row['chord'].strip(),
                    'start': float(row['start']),
                    'end': float(row['end'])
                }
                
                # Validaciones adicionales
                if not chord_data['chord']:
                    invalid_rows.append(f"Fila {i+2}: Acorde vacío")
                    continue
                
                if chord_data['start'] < 0 or chord_data['end'] < 0:
                    invalid_rows.append(f"Fila {i+2}: Tiempos negativos no permitidos")
                    continue
                
                if chord_data['start'] >= chord_data['end']:
                    invalid_rows.append(f"Fila {i+2}: Tiempo de inicio debe ser menor que tiempo de fin")
                    continue
                
                chords.append(chord_data)
                
            except ValueError as e:
                invalid_rows.append(f"Fila {i+2}: Error en formato numérico - {e}")
            except KeyError as e:
                invalid_rows.append(f"Fila {i+2}: Columna faltante - {e}")
        
        # Mostrar advertencias sobre filas inválidas
        if invalid_rows:
            st.warning(f"Se omitieron {len(invalid_rows)} filas con errores:")
            for error in invalid_rows[:5]:  # Mostrar solo los primeros 5 errores
                st.caption(f"⚠️ {error}")
            if len(invalid_rows) > 5:
                st.caption(f"... y {len(invalid_rows) - 5} errores más")
        
        if not chords:
            st.error("No se pudo procesar ninguna fila válida del archivo")
            return []
        
    except UnicodeDecodeError:
        st.error("Error de codificación. Asegúrate de que el archivo esté en formato UTF-8")
        return []
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return []
    
    return chords

def simplify_chord(chord):
    """Simplificar notación de acordes"""
    if ':maj' in chord:
        return chord.replace(':maj', '')
    elif ':min' in chord:
        return chord.replace(':min', 'm')
    else:
        return chord

def convert_to_beats(chords, bpm):
    """Convertir tiempos en segundos a beats"""
    for c in chords:
        c['start_beat'] = c['start'] * (bpm / 60.0)
        c['end_beat'] = c['end'] * (bpm / 60.0)
    return chords

def generate_chord_chart(chords, bpm, beats_per_measure, measures_per_line, chars_per_beat):
    """Generar el chart de acordes como texto"""
    if not chords:
        return "No hay datos de acordes disponibles"
    
    # Convertir a beats
    chords = convert_to_beats(chords.copy(), bpm)
    
    # Simplificar acordes
    for c in chords:
        c['chord'] = simplify_chord(c['chord'])
    
    # Calcular total de medidas
    max_beat = max(c['end_beat'] for c in chords)
    total_measures = int(max_beat // beats_per_measure) + 1
    
    chart_lines = []
    current_measure = 0
    
    while current_measure < total_measures:
        start_measure = current_measure
        end_measure = min(start_measure + measures_per_line, total_measures)
        
        start_beat = start_measure * beats_per_measure
        end_beat = end_measure * beats_per_measure
        
        # Calcular longitud de la línea
        line_length = int((end_beat - start_beat) * chars_per_beat)
        
        # Inicializar líneas
        chord_line = [' '] * line_length
        bar_line = ['/'] * line_length
        
        # Colocar barras de compás
        for m in range(start_measure, end_measure + 1):
            beat_pos = (m - start_measure) * beats_per_measure
            char_pos = int(beat_pos * chars_per_beat)
            if char_pos < line_length:
                bar_line[char_pos] = '|'
        
        # Colocar acordes en sus start_beat
        for c in chords:
            if start_beat <= c['start_beat'] < end_beat:
                beat_pos = c['start_beat'] - start_beat
                char_pos = int(beat_pos * chars_per_beat)
                chord = c['chord']
                # Limpiar espacio para el acorde
                for i in range(len(chord)):
                    if char_pos + i < line_length:
                        chord_line[char_pos + i] = ' '
                # Colocar el acorde
                for i, char in enumerate(chord):
                    if char_pos + i < line_length:
                        chord_line[char_pos + i] = char
        
        # Agregar números de compás
        measure_line = [' '] * line_length
        for m in range(start_measure, end_measure):
            beat_pos = (m - start_measure) * beats_per_measure
            char_pos = int(beat_pos * chars_per_beat)
            measure_num = str(m + 1)
            if char_pos < line_length:
                measure_line[char_pos] = measure_num[0] if len(measure_num) == 1 else measure_num[0]
                if len(measure_num) > 1 and char_pos + 1 < line_length:
                    measure_line[char_pos + 1] = measure_num[1]
        
        # Unir líneas
        chord_str = ''.join(chord_line)
        bar_str = ''.join(bar_line)
        measure_str = ''.join(measure_line)
        
        # Agregar al chart
        chart_lines.append(chord_str)
        chart_lines.append(bar_str)
        chart_lines.append(measure_str)
        chart_lines.append('')  # Línea vacía entre sistemas
        
        current_measure = end_measure
    
    return '\n'.join(chart_lines)

def generate_pdf(chart_text, title="Chord Chart"):
    """Generar PDF del chart"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font("Arial", 'B', 16)
        # Limpiar título de caracteres problemáticos
        clean_title = title.encode('latin-1', errors='replace').decode('latin-1')
        pdf.cell(0, 10, clean_title, ln=True, align='C')
        pdf.ln(5)
        
        # Chart
        pdf.set_font("Courier", size=9)  # Reducir tamaño para mejor ajuste
        lines = chart_text.split('\n')
        
        for line in lines:
            # Limpiar línea de caracteres problemáticos
            clean_line = line.encode('latin-1', errors='replace').decode('latin-1')
            # Truncar líneas muy largas
            if len(clean_line) > 100:
                clean_line = clean_line[:100] + "..."
            
            try:
                pdf.cell(0, 4, clean_line, ln=True)
            except:
                # Si falla, usar una línea simplificada
                pdf.cell(0, 4, line[:50] + "...", ln=True)
        
        return pdf
    except Exception as e:
        # Crear PDF básico en caso de error
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Error al generar chart", ln=True, align='C')
        pdf.cell(0, 10, f"Error: {str(e)}", ln=True, align='C')
        return pdf

def get_pdf_download_link(pdf, filename):
    """Crear enlace de descarga para PDF"""
    try:
        # Usar BytesIO directamente para evitar problemas de codificación
        pdf_bytes = pdf.output(dest='S')
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode('latin-1', errors='replace')
        
        b64 = base64.b64encode(pdf_bytes).decode()
        
        # Limpiar el nombre del archivo para evitar caracteres problemáticos
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._- ").strip()
        if not safe_filename.endswith('.pdf'):
            safe_filename += '.pdf'
        
        href = f'<a href="data:application/pdf;base64,{b64}" download="{safe_filename}" style="text-decoration: none; background-color: #4CAF50; color: white; padding: 8px 16px; border-radius: 4px; display: inline-block;">📄 Descargar PDF</a>'
        return href
    except Exception as e:
        st.error(f"Error al crear enlace de descarga: {e}")
        return f"<p>Error al generar enlace de descarga</p>"

# Interfaz de Streamlit
def main():
    st.set_page_config(page_title="Generador de Chart de Acordes", layout="wide")
    
    st.title("🎵 Generador de Chart de Acordes")
    st.markdown("---")
    
    # Pestañas para diferentes opciones de carga
    tab1, tab2 = st.tabs(["📂 Archivos locales", "⬆️ Subir archivo CSV"])
    
    chords = []
    file_source = ""
    
    with tab1:
        st.markdown("### Seleccionar archivo CSV del directorio actual")
        # Cargar archivo CSV local
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        
        if csv_files:
            selected_file = st.selectbox("Archivos CSV disponibles:", csv_files)
            if st.button("Cargar archivo seleccionado", type="secondary"):
                chords = load_chord_data(selected_file)
                file_source = selected_file
        else:
            st.warning("No se encontraron archivos CSV en el directorio actual")
    
    with tab2:
        st.markdown("### Subir un archivo CSV nuevo")
        
        # Mostrar ejemplo del formato
        with st.expander("📋 Ver formato requerido del archivo CSV"):
            st.markdown("**El archivo CSV debe tener exactamente estas columnas:**")
            example_csv = """chord,start,end
G:maj,0.650158726,2.972154176
G:min,3.018594085,3.947392265
A:min,6.315827624,6.919546441
D:maj,8.123456789,10.987654321"""
            
            st.code(example_csv, language="csv")
            
            st.markdown("""
            **Descripción de las columnas:**
            - **chord**: Nombre del acorde (ej: G:maj, A:min, C:maj)
            - **start**: Tiempo de inicio en segundos (número decimal)
            - **end**: Tiempo de finalización en segundos (número decimal)
            
            **Notas importantes:**
            - El archivo debe usar comas como separador
            - Los tiempos deben ser números positivos
            - El tiempo de inicio debe ser menor que el de finalización
            - Los acordes se simplificarán automáticamente (:maj → "", :min → "m")
            """)
        
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV",
            type=['csv'],
            help="El archivo debe tener las columnas: chord, start, end"
        )
        
        if uploaded_file is not None:
            # Mostrar información del archivo
            st.info(f"📄 Archivo: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            # Cargar y procesar el archivo
            chords = load_chord_data_from_uploaded_file(uploaded_file)
            file_source = uploaded_file.name
            
            # Mostrar preview de los primeros registros
            if chords:
                st.markdown("#### 👀 Preview de los datos:")
                preview_df = pd.DataFrame(chords[:5])  # Mostrar solo los primeros 5
                st.dataframe(preview_df, use_container_width=True)
                
                if len(chords) > 5:
                    st.caption(f"Mostrando 5 de {len(chords)} registros")
                
                # Botón para descargar CSV de ejemplo
                st.download_button(
                    label="💾 Descargar CSV de ejemplo",
                    data=example_csv,
                    file_name="ejemplo_acordes.csv",
                    mime="text/csv",
                    help="Descarga un archivo CSV de ejemplo para usar como plantilla"
                )
    
    # Verificar si se cargaron datos
    if not chords:
        st.info("👆 Selecciona una pestaña arriba para cargar un archivo CSV")
        st.stop()
    
    st.success(f"✅ Cargados {len(chords)} acordes desde **{file_source}**")
    
    # Configuraciones en sidebar
    st.sidebar.header("⚙️ Configuraciones")
    
    bpm = st.sidebar.number_input("BPM (Beats por minuto)", min_value=60, max_value=200, value=120, step=5)
    beats_per_measure = st.sidebar.selectbox("Beats por compás", [3, 4, 6, 8], index=1)
    measures_per_line = st.sidebar.number_input("Compases por línea", min_value=2, max_value=8, value=4, step=1)
    chars_per_beat = st.sidebar.slider("Espaciado (caracteres por beat)", min_value=4, max_value=12, value=8, step=1)
    
    # Mostrar información de la canción
    if chords:
        duration = max(c['end'] for c in chords)
        unique_chords = list(set([simplify_chord(c['chord']) for c in chords]))
        
        st.sidebar.markdown("### 📊 Información de la canción")
        st.sidebar.metric("Duración", f"{duration:.1f} segundos", f"{duration/60:.1f} minutos")
        st.sidebar.metric("Total acordes", len(chords))
        st.sidebar.metric("Acordes únicos", len(unique_chords))
        
        # Mostrar acordes más frecuentes
        chord_counts = {}
        for chord in chords:
            simplified = simplify_chord(chord['chord'])
            chord_counts[simplified] = chord_counts.get(simplified, 0) + 1
        
        most_common = sorted(chord_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        st.sidebar.markdown("**Acordes más frecuentes:**")
        for chord, count in most_common:
            st.sidebar.write(f"• {chord}: {count} veces")
        
        # Mostrar todos los acordes únicos
        with st.sidebar.expander("Ver todos los acordes únicos"):
            st.write(", ".join(sorted(unique_chords)))
        
        # Información adicional del archivo
        st.sidebar.markdown("---")
        st.sidebar.markdown("**📁 Archivo cargado:**")
        st.sidebar.write(f"• **Nombre:** {file_source}")
        st.sidebar.write(f"• **Primer acorde:** {simplify_chord(chords[0]['chord'])}")
        st.sidebar.write(f"• **Último acorde:** {simplify_chord(chords[-1]['chord'])}")
    
    # Generar chart
    st.markdown("### 🎼 Chart de Acordes")
    
    chart_text = generate_chord_chart(chords, bpm, beats_per_measure, measures_per_line, chars_per_beat)
    
    # Mostrar chart en un código block para mantener formato
    st.code(chart_text, language=None)
    
    # Botón para generar PDF
    st.markdown("### 📄 Exportar a PDF")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Método 1: Botón de descarga nativo de Streamlit (más confiable)
        try:
            pdf = generate_pdf(chart_text, f"Chart de Acordes - {file_source}")
            pdf_bytes = pdf.output(dest='S')
            if isinstance(pdf_bytes, str):
                pdf_bytes = pdf_bytes.encode('latin-1', errors='replace')
            
            clean_filename = file_source.replace('.csv', '').replace(' ', '_')
            pdf_filename = f"chord_chart_{clean_filename}.pdf"
            
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                type="primary"
            )
            
        except Exception as e:
            st.error(f"Error al preparar PDF: {e}")
    
    with col2:
        # Método alternativo usando enlace HTML
        if st.button("🔗 Generar enlace de descarga", type="secondary"):
            try:
                pdf = generate_pdf(chart_text, f"Chart de Acordes - {file_source}")
                clean_filename = file_source.replace('.csv', '').replace(' ', '_')
                pdf_filename = f"chord_chart_{clean_filename}.pdf"
                pdf_link = get_pdf_download_link(pdf, pdf_filename)
                st.markdown(pdf_link, unsafe_allow_html=True)
                st.success("Enlace de descarga generado!")
            except Exception as e:
                st.error(f"Error al generar enlace: {e}")
                st.info("Usa el botón 'Descargar PDF' de la izquierda como alternativa")

if __name__ == "__main__":
    main()
