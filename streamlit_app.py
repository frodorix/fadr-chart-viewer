import streamlit as st
import pandas as pd
import csv
from fpdf import FPDF
import base64
import io
import os
import numpy as np
import wave
import struct
import math

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

# Funciones para generar audio de escalas
def note_to_frequency(note_name):
    """Convertir nombre de nota a frecuencia en Hz"""
    # Mapeo de notas a semitonos desde A4 (440 Hz)
    note_mapping = {
        'C': -9, 'C#': -8, 'Db': -8,
        'D': -7, 'D#': -6, 'Eb': -6,
        'E': -5,
        'F': -4, 'F#': -3, 'Gb': -3,
        'G': -2, 'G#': -1, 'Ab': -1,
        'A': 0, 'A#': 1, 'Bb': 1,
        'B': 2
    }
    
    # Extraer nota base (sin octava)
    if len(note_name) > 1 and note_name[1] in ['#', 'b']:
        base_note = note_name[:2]
        octave = int(note_name[2:]) if len(note_name) > 2 else 4
    else:
        base_note = note_name[0]
        octave = int(note_name[1:]) if len(note_name) > 1 else 4
    
    if base_note not in note_mapping:
        return 440.0  # Default to A4
    
    # Calcular semitonos desde A4
    semitones = note_mapping[base_note] + (octave - 4) * 12
    
    # Calcular frecuencia usando la fórmula: f = 440 * 2^(n/12)
    frequency = 440.0 * (2 ** (semitones / 12.0))
    return frequency

def get_scale_notes(chord_name):
    """Obtener las notas de la escala para un acorde dado"""
    # Simplificar el nombre del acorde
    chord_name = simplify_chord(chord_name)
    
    # Extraer nota raíz
    if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
        root = chord_name[:2]
        chord_type = chord_name[2:]
    else:
        root = chord_name[0]
        chord_type = chord_name[1:]
    
    # Definir intervalos de escalas (en semitonos)
    scale_intervals = {
        '': [0, 2, 4, 5, 7, 9, 11],        # Mayor
        'maj': [0, 2, 4, 5, 7, 9, 11],     # Mayor
        'm': [0, 2, 3, 5, 7, 8, 10],       # Menor natural
        'min': [0, 2, 3, 5, 7, 8, 10],     # Menor natural
        '7': [0, 2, 4, 5, 7, 9, 10],       # Dominante
        'maj7': [0, 2, 4, 5, 7, 9, 11],    # Mayor séptima
        'm7': [0, 2, 3, 5, 7, 8, 10],      # Menor séptima
    }
    
    intervals = scale_intervals.get(chord_type.lower(), scale_intervals[''])
    
    # Nota raíz a número MIDI (C4 = 60)
    note_to_midi = {
        'C': 60, 'C#': 61, 'Db': 61,
        'D': 62, 'D#': 63, 'Eb': 63,
        'E': 64,
        'F': 65, 'F#': 66, 'Gb': 66,
        'G': 67, 'G#': 68, 'Ab': 68,
        'A': 69, 'A#': 70, 'Bb': 70,
        'B': 71
    }
    
    root_midi = note_to_midi.get(root, 60)
    
    # Generar notas de la escala
    scale_notes = []
    for interval in intervals:
        midi_note = root_midi + interval
        frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
        scale_notes.append(frequency)
    
    return scale_notes

def generate_piano_harmonics(frequency, t, amplitude=0.3):
    """Generar armónicos para simular sonido de piano"""
    # Armónicos más realistas del piano con amplitudes más suaves
    harmonics = [
        (1.0, 1.0),      # Fundamental
        (2.0, 0.4),      # Segunda armónica (reducida)
        (3.0, 0.15),     # Tercera armónica (reducida)
        (4.0, 0.08),     # Cuarta armónica (reducida)
        (5.0, 0.04),     # Quinta armónica (reducida)
        (6.0, 0.02),     # Sexta armónica (reducida)
    ]
    
    wave = np.zeros_like(t)
    for harmonic_freq, harmonic_amp in harmonics:
        # Añadir slight detuning natural para realismo (muy sutil)
        detuning = 1.0 + (harmonic_freq - 1) * 0.001  # Muy pequeño desajuste
        wave += harmonic_amp * np.sin(2 * np.pi * frequency * harmonic_freq * detuning * t)
    
    return amplitude * wave

def generate_piano_envelope(duration_seconds, sample_rate):
    """Generar envolvente ADSR típica del piano"""
    total_samples = int(sample_rate * duration_seconds)
    
    # Parámetros ADSR más suaves para piano
    attack_time = 0.005   # 5ms attack muy rápido
    decay_time = 0.15     # 150ms decay más suave
    sustain_level = 0.8   # 80% del volumen máximo (más alto)
    release_time = min(0.4, duration_seconds * 0.5)  # Release suave
    
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    sustain_samples = max(0, total_samples - attack_samples - decay_samples - release_samples)
    
    envelope = np.ones(total_samples)
    
    # Attack: 0 a 1 con curva exponencial suave
    if attack_samples > 0:
        attack_curve = np.linspace(0, 1, attack_samples)
        # Aplicar curva exponencial para ataque más natural
        attack_curve = 1 - np.exp(-5 * attack_curve)
        envelope[:attack_samples] = attack_curve
    
    # Decay: 1 a sustain_level con curva exponencial
    if decay_samples > 0:
        start_idx = attack_samples
        end_idx = start_idx + decay_samples
        decay_curve = np.linspace(0, 1, decay_samples)
        # Curva exponencial para decay más natural
        decay_curve = np.exp(-2 * decay_curve)
        envelope[start_idx:end_idx] = sustain_level + (1 - sustain_level) * decay_curve
    
    # Sustain: mantener sustain_level
    if sustain_samples > 0:
        start_idx = attack_samples + decay_samples
        end_idx = start_idx + sustain_samples
        envelope[start_idx:end_idx] = sustain_level
    
    # Release: sustain_level a 0 con curva exponencial suave
    if release_samples > 0:
        start_idx = total_samples - release_samples
        release_curve = np.linspace(0, 1, release_samples)
        # Curva exponencial para release más natural
        release_curve = sustain_level * np.exp(-3 * release_curve)
        envelope[start_idx:] = release_curve
    
    return envelope

def generate_tone(frequency, duration_ms, sample_rate=44100, amplitude=0.3, instrument="piano"):
    """Generar un tono con diferentes tipos de instrumento"""
    duration_seconds = duration_ms / 1000.0
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    
    if instrument == "piano":
        # Generar sonido de piano con armónicos (SIN vibrato)
        wave_data = generate_piano_harmonics(frequency, t, amplitude)
        
        # Aplicar envolvente ADSR del piano
        envelope = generate_piano_envelope(duration_seconds, sample_rate)
        wave_data *= envelope
        
    elif instrument == "sine":
        # Tono senoidal simple (original)
        wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Aplicar envolvente simple
        envelope_length = int(0.01 * sample_rate)  # 10ms fade
        if len(wave_data) > 2 * envelope_length:
            wave_data[:envelope_length] *= np.linspace(0, 1, envelope_length)
            wave_data[-envelope_length:] *= np.linspace(1, 0, envelope_length)
    
    elif instrument == "organ":
        # Sonido de órgano con armónicos específicos
        wave_data = amplitude * (
            np.sin(2 * np.pi * frequency * t) +
            0.5 * np.sin(2 * np.pi * frequency * 2 * t) +
            0.3 * np.sin(2 * np.pi * frequency * 3 * t)
        )
        
        # Envolvente más sostenida para órgano
        envelope_length = int(0.05 * sample_rate)
        if len(wave_data) > 2 * envelope_length:
            wave_data[:envelope_length] *= np.linspace(0, 1, envelope_length)
            wave_data[-envelope_length:] *= np.linspace(1, 0, envelope_length)
    
    return wave_data

def generate_scale_audio(chord_name, note_duration_ms=700, repetitions=1, ascending=True, descending=True, instrument="piano"):
    """Generar audio de escala para un acorde"""
    try:
        scale_frequencies = get_scale_notes(chord_name)
        sample_rate = 44100
        
        # Crear secuencia de notas
        sequence = []
        
        for rep in range(repetitions):
            if ascending:
                sequence.extend(scale_frequencies)
            if descending:
                sequence.extend(reversed(scale_frequencies))
        
        # Generar audio completo
        audio_data = []
        silence_duration_ms = 50  # Pequeña pausa entre notas
        
        for i, frequency in enumerate(sequence):
            # Generar tono con el instrumento seleccionado
            tone = generate_tone(frequency, note_duration_ms, sample_rate, instrument=instrument)
            audio_data.extend(tone)
            
            # Añadir pequeña pausa entre notas (excepto la última)
            if i < len(sequence) - 1:
                silence_samples = int(silence_duration_ms * sample_rate / 1000)
                audio_data.extend(np.zeros(silence_samples))
        
        # Convertir a array de numpy
        audio_array = np.array(audio_data)
        
        # Normalizar
        if np.max(np.abs(audio_array)) > 0:
            audio_array = audio_array / np.max(np.abs(audio_array)) * 0.8
        
        # Convertir a 16-bit PCM
        audio_16bit = (audio_array * 32767).astype(np.int16)
        
        return audio_16bit, sample_rate
        
    except Exception as e:
        st.error(f"Error generando audio: {e}")
        return None, None

def save_wav_file(audio_data, sample_rate, filename):
    """Guardar audio como archivo WAV"""
    try:
        # Crear archivo WAV en memoria
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        wav_buffer.seek(0)
        return wav_buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error guardando archivo WAV: {e}")
        return None

# Interfaz de Streamlit
def main():
    st.set_page_config(page_title="Generador de Chart de Acordes", layout="wide")
    
    st.title("🎵 Generador de Chart de Acordes")
    st.markdown("---")
    
    # Menú principal con diferentes funcionalidades
    menu_option = st.selectbox(
        "Selecciona una funcionalidad:",
        ["📊 Generar Chart de Acordes", "🎵 Generar Audio de Escalas"],
        index=1
    )
    
    if menu_option == "📊 Generar Chart de Acordes":
        generate_chord_chart_interface()
    elif menu_option == "🎵 Generar Audio de Escalas":
        generate_scale_audio_interface()

def generate_scale_audio_interface():
    """Interfaz para generar audio de escalas"""
    st.markdown("### 🎵 Generador de Audio de Escalas")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### ⚙️ Configuración de la Escala")
        
        # Input para el nombre del acorde
        chord_name = st.text_input(
            "Nombre del acorde:",
            value="C",
            help="Ejemplos: C, Dm, G7, Fmaj7, Am, etc."
        )
        
        # Configuraciones de tiempo
        note_duration = st.slider(
            "Duración por nota (milisegundos):",
            min_value=200,
            max_value=2000,
            value=700,
            step=50,
            help="Tiempo que dura cada nota de la escala"
        )
        
        repetitions = st.number_input(
            "Número de repeticiones:",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )
        
        # Selección de instrumento
        st.markdown("**Tipo de instrumento:**")
        instrument = st.selectbox(
            "Sonido:",
            ["piano", "sine", "organ"],
            index=0,
            help="Selecciona el tipo de sonido para las notas"
        )
        
        # Mostrar descripción del instrumento
        instrument_descriptions = {
            "piano": "🎹 Piano - Sonido suave con armónicos naturales y envolvente realista",
            "sine": "〰️ Senoidal - Tono puro y limpio (original)",
            "organ": "🎼 Órgano - Sonido sostenido con armónicos ricos"
        }
        st.caption(instrument_descriptions[instrument])
        
        # Opciones de dirección
        st.markdown("**Dirección de la escala:**")
        ascending = st.checkbox("Ascendente", value=True)
        descending = st.checkbox("Descendente", value=True)
        
        if not ascending and not descending:
            st.warning("Selecciona al menos una dirección (ascendente o descendente)")
        
        # Información sobre el acorde
        if chord_name.strip():
            simplified = simplify_chord(chord_name.strip())
            st.info(f"Acorde simplificado: **{simplified}**")
            
            try:
                scale_frequencies = get_scale_notes(chord_name.strip())
                st.success(f"✅ Escala válida con {len(scale_frequencies)} notas")
            except:
                st.error("⚠️ Nombre de acorde no reconocido")
    
    with col2:
        st.markdown("#### 🎼 Generar Audio")
        
        if st.button("🎵 Generar Audio de Escala", type="primary", disabled=not (ascending or descending)):
            if chord_name.strip():
                with st.spinner("Generando audio..."):
                    try:
                        # Generar audio
                        audio_data, sample_rate = generate_scale_audio(
                            chord_name.strip(),
                            note_duration,
                            repetitions,
                            ascending,
                            descending,
                            instrument
                        )
                        
                        if audio_data is not None:
                            # Guardar como WAV
                            wav_data = save_wav_file(audio_data, sample_rate, "scale_audio.wav")
                            
                            if wav_data:
                                # Mostrar reproductor de audio
                                st.success("🎉 Audio generado exitosamente!")
                                st.audio(wav_data, format="audio/wav")
                                
                                # Botón de descarga
                                filename = f"escala_{chord_name.strip().replace(':', '_')}_{instrument}_{note_duration}ms.wav"
                                st.download_button(
                                    label="💾 Descargar Audio WAV",
                                    data=wav_data,
                                    file_name=filename,
                                    mime="audio/wav"
                                )
                                
                                # Información del archivo generado
                                scale_notes = get_scale_notes(chord_name.strip())
                                duration_total = len(scale_notes) * note_duration * repetitions
                                if ascending and descending:
                                    duration_total *= 2
                                
                                st.markdown(f"""
                                **📊 Información del audio:**
                                - **Acorde:** {simplify_chord(chord_name.strip())}
                                - **Instrumento:** {instrument_descriptions[instrument].split(' - ')[1]}
                                - **Notas por escala:** {len(scale_notes)}
                                - **Duración por nota:** {note_duration} ms
                                - **Repeticiones:** {repetitions}
                                - **Duración total:** ~{duration_total/1000:.1f} segundos
                                """)
                            else:
                                st.error("Error al procesar el audio")
                        else:
                            st.error("No se pudo generar el audio")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Por favor ingresa un nombre de acorde")
        
        # Ayuda sobre nombres de acordes
        with st.expander("📋 Ayuda - Nombres de acordes válidos"):
            st.markdown("""
            **Ejemplos de acordes válidos:**
            
            **Acordes básicos:**
            - `C`, `D`, `E`, `F`, `G`, `A`, `B`
            - `Cm`, `Dm`, `Em`, `Am` (menores)
            
            **Con alteraciones:**
            - `C#`, `Db`, `F#`, `Gb`, `A#`, `Bb`
            - `C#m`, `Ebm`, `F#m` (menores con alteraciones)
            
            **Acordes de séptima:**
            - `C7`, `G7`, `D7` (dominantes)
            - `Cmaj7`, `Fmaj7` (mayores con séptima)
            - `Cm7`, `Am7` (menores con séptima)
            
            **Notas:**
            - Los acordes se simplifican automáticamente
            - `:maj` se convierte en acorde mayor
            - `:min` se convierte en `m` (menor)
            - Si no se especifica tipo, se asume mayor
            """)

def generate_chord_chart_interface():
    """Interfaz para generar charts de acordes"""
    st.markdown("### 📊 Generador de Chart de Acordes")
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
