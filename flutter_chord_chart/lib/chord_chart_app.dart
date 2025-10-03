import 'package:flutter/material.dart';
import 'models/chord_data.dart';
import 'services/csv_service.dart';
import 'services/pdf_service.dart';
import 'widgets/chord_chart_widget.dart';

class ChordChartApp extends StatefulWidget {
  const ChordChartApp({Key? key}) : super(key: key);

  @override
  State<ChordChartApp> createState() => _ChordChartAppState();
}

class _ChordChartAppState extends State<ChordChartApp> {
  List<ChordData> chords = [];
  double bpm = 120.0;
  int beatsPerMeasure = 4;
  int measuresPerLine = 4;
  double charsPerBeat = 8.0;
  String fileName = '';
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadDefaultCsv();
  }

  Future<void> _loadDefaultCsv() async {
    // Intentar cargar el CSV por defecto si existe
    try {
      const defaultCsvContent = '''chord,start,end
G:maj,0.650158726,2.972154176
G:min,3.018594085,3.947392265
G:min,3.993832174,4.551111082
G:maj,4.597550991,6.269387715000001
A:min,6.315827624000001,6.9195464410000005
G:maj,6.9659863500000005,12.956734611''';
      
      List<ChordData> defaultChords = CsvService.loadChordDataFromString(defaultCsvContent);
      if (defaultChords.isNotEmpty) {
        setState(() {
          chords = defaultChords;
          fileName = 'Datos de ejemplo';
        });
      }
    } catch (e) {
      print('Error cargando datos por defecto: $e');
    }
  }

  Future<void> _loadCsvFile() async {
    setState(() {
      isLoading = true;
    });

    try {
      List<ChordData>? loadedChords = await CsvService.loadChordDataFromFile();
      if (loadedChords != null && loadedChords.isNotEmpty) {
        setState(() {
          chords = loadedChords;
          fileName = 'Archivo cargado exitosamente';
        });
      } else {
        _showSnackBar('No se pudo cargar el archivo CSV o está vacío');
      }
    } catch (e) {
      _showSnackBar('Error al cargar archivo: $e');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _exportToPdf() async {
    if (chords.isEmpty) {
      _showSnackBar('No hay datos para exportar');
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      await PdfService.generateAndSharePdf(
        chords: chords,
        bpm: bpm,
        beatsPerMeasure: beatsPerMeasure,
        measuresPerLine: measuresPerLine,
        charsPerBeat: charsPerBeat,
        title: 'Chord Chart - $fileName',
      );
    } catch (e) {
      _showSnackBar('Error al exportar PDF: $e');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _printPdf() async {
    if (chords.isEmpty) {
      _showSnackBar('No hay datos para imprimir');
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      await PdfService.printPdf(
        chords: chords,
        bpm: bpm,
        beatsPerMeasure: beatsPerMeasure,
        measuresPerLine: measuresPerLine,
        charsPerBeat: charsPerBeat,
        title: 'Chord Chart - $fileName',
      );
    } catch (e) {
      _showSnackBar('Error al imprimir: $e');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  Widget _buildControlPanel() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Configuración',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            
            // Cargar archivo
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: isLoading ? null : _loadCsvFile,
                    icon: const Icon(Icons.folder_open),
                    label: const Text('Cargar CSV'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Text(
                    fileName.isEmpty ? 'Ningún archivo cargado' : fileName,
                    style: Theme.of(context).textTheme.bodyMedium,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            // Controles de configuración
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('BPM: ${bpm.round()}'),
                      Slider(
                        value: bpm,
                        min: 60,
                        max: 200,
                        divisions: 28,
                        onChanged: (value) {
                          setState(() {
                            bpm = value;
                          });
                        },
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Beats por compás'),
                      DropdownButton<int>(
                        value: beatsPerMeasure,
                        isExpanded: true,
                        items: [3, 4, 6, 8].map((value) {
                          return DropdownMenuItem(
                            value: value,
                            child: Text('$value'),
                          );
                        }).toList(),
                        onChanged: (value) {
                          if (value != null) {
                            setState(() {
                              beatsPerMeasure = value;
                            });
                          }
                        },
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Compases por línea: $measuresPerLine'),
                      Slider(
                        value: measuresPerLine.toDouble(),
                        min: 2,
                        max: 8,
                        divisions: 6,
                        onChanged: (value) {
                          setState(() {
                            measuresPerLine = value.round();
                          });
                        },
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Espaciado: ${charsPerBeat.round()}'),
                      Slider(
                        value: charsPerBeat,
                        min: 4,
                        max: 12,
                        divisions: 8,
                        onChanged: (value) {
                          setState(() {
                            charsPerBeat = value;
                          });
                        },
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            // Información de la canción
            if (chords.isNotEmpty) ...[
              const Divider(),
              Text(
                'Información de la canción',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(
                    children: [
                      Text('${chords.length}', style: Theme.of(context).textTheme.headlineSmall),
                      const Text('Acordes'),
                    ],
                  ),
                  Column(
                    children: [
                      Text('${(chords.last.end).toStringAsFixed(1)}s', 
                           style: Theme.of(context).textTheme.headlineSmall),
                      const Text('Duración'),
                    ],
                  ),
                  Column(
                    children: [
                      Text('${chords.map((c) => c.simplifiedChord).toSet().length}', 
                           style: Theme.of(context).textTheme.headlineSmall),
                      const Text('Únicos'),
                    ],
                  ),
                ],
              ),
            ],
            const SizedBox(height: 16),
            
            // Botones de acción
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: (isLoading || chords.isEmpty) ? null : _printPdf,
                    icon: const Icon(Icons.print),
                    label: const Text('Vista Previa/Imprimir'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: (isLoading || chords.isEmpty) ? null : _exportToPdf,
                    icon: const Icon(Icons.share),
                    label: const Text('Exportar PDF'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🎵 Generador de Chart de Acordes'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Row(
              children: [
                // Panel de control (lado izquierdo)
                SizedBox(
                  width: 400,
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: _buildControlPanel(),
                  ),
                ),
                
                // Área de preview (lado derecho)
                Expanded(
                  child: Container(
                    margin: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.grey.shade300),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.grey.shade100,
                            borderRadius: const BorderRadius.only(
                              topLeft: Radius.circular(8),
                              topRight: Radius.circular(8),
                            ),
                          ),
                          child: Text(
                            '🎼 Preview del Chart',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                        ),
                        Expanded(
                          child: chords.isEmpty
                              ? const Center(
                                  child: Text(
                                    'Carga un archivo CSV para ver el preview',
                                    style: TextStyle(
                                      fontSize: 16,
                                      color: Colors.grey,
                                    ),
                                  ),
                                )
                              : SingleChildScrollView(
                                  padding: const EdgeInsets.all(16),
                                  child: Container(
                                    height: 600,
                                    child: ChordChartWidget(
                                      chords: chords,
                                      bpm: bpm,
                                      beatsPerMeasure: beatsPerMeasure,
                                      measuresPerLine: measuresPerLine,
                                      charsPerBeat: charsPerBeat,
                                    ),
                                  ),
                                ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
    );
  }
}