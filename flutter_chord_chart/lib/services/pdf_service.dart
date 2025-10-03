import 'dart:io';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';
import '../models/chord_data.dart';

class PdfService {
  static Future<void> generateAndSharePdf({
    required List<ChordData> chords,
    required double bpm,
    required int beatsPerMeasure,
    required int measuresPerLine,
    required double charsPerBeat,
    required String title,
  }) async {
    final pdf = pw.Document();
    
    // Calcular beats para todos los acordes
    for (var chord in chords) {
      chord.calculateBeats(bpm);
    }

    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              // Título
              pw.Container(
                alignment: pw.Alignment.center,
                child: pw.Text(
                  title,
                  style: pw.TextStyle(
                    fontSize: 18,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
              ),
              pw.SizedBox(height: 20),
              
              // Chart
              pw.Expanded(
                child: _buildPdfChart(
                  chords: chords,
                  bpm: bpm,
                  beatsPerMeasure: beatsPerMeasure,
                  measuresPerLine: measuresPerLine,
                  charsPerBeat: charsPerBeat,
                ),
              ),
            ],
          );
        },
      ),
    );

    final output = await getTemporaryDirectory();
    final file = File('${output.path}/chord_chart.pdf');
    await file.writeAsBytes(await pdf.save());

    await Share.shareXFiles([XFile(file.path)], text: 'Chord Chart');
  }

  static Future<void> printPdf({
    required List<ChordData> chords,
    required double bpm,
    required int beatsPerMeasure,
    required int measuresPerLine,
    required double charsPerBeat,
    required String title,
  }) async {
    final pdf = pw.Document();
    
    // Calcular beats para todos los acordes
    for (var chord in chords) {
      chord.calculateBeats(bpm);
    }

    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Container(
                alignment: pw.Alignment.center,
                child: pw.Text(
                  title,
                  style: pw.TextStyle(
                    fontSize: 18,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
              ),
              pw.SizedBox(height: 20),
              
              pw.Expanded(
                child: _buildPdfChart(
                  chords: chords,
                  bpm: bpm,
                  beatsPerMeasure: beatsPerMeasure,
                  measuresPerLine: measuresPerLine,
                  charsPerBeat: charsPerBeat,
                ),
              ),
            ],
          );
        },
      ),
    );

    await Printing.layoutPdf(onLayout: (PdfPageFormat format) async => pdf.save());
  }

  static pw.Widget _buildPdfChart({
    required List<ChordData> chords,
    required double bpm,
    required int beatsPerMeasure,
    required int measuresPerLine,
    required double charsPerBeat,
  }) {
    if (chords.isEmpty) {
      return pw.Text('No hay datos de acordes disponibles');
    }

    List<pw.Widget> chartLines = [];
    
    // Calcular total de medidas
    double maxBeat = chords.map((c) => c.endBeat).reduce((a, b) => a > b ? a : b);
    int totalMeasures = (maxBeat / beatsPerMeasure).ceil();

    int currentMeasure = 0;

    while (currentMeasure < totalMeasures) {
      int startMeasure = currentMeasure;
      int endMeasure = (startMeasure + measuresPerLine).clamp(0, totalMeasures);
      
      double startBeat = startMeasure * beatsPerMeasure.toDouble();
      double endBeat = endMeasure * beatsPerMeasure.toDouble();
      
      // Construir línea de acordes
      String chordLine = _buildChordLine(chords, startBeat, endBeat, beatsPerMeasure, charsPerBeat, startMeasure);
      String barLine = _buildBarLine(startMeasure, endMeasure, beatsPerMeasure, charsPerBeat);
      String measureLine = _buildMeasureLine(startMeasure, endMeasure, beatsPerMeasure, charsPerBeat);

      chartLines.add(
        pw.Column(
          crossAxisAlignment: pw.CrossAxisAlignment.start,
          children: [
            pw.Text(chordLine, style: pw.TextStyle(fontFamily: pw.Font.courier(), fontSize: 10)),
            pw.Text(barLine, style: pw.TextStyle(fontFamily: pw.Font.courier(), fontSize: 10)),
            pw.Text(measureLine, style: pw.TextStyle(fontFamily: pw.Font.courier(), fontSize: 8)),
            pw.SizedBox(height: 8),
          ],
        ),
      );

      currentMeasure = endMeasure;
    }

    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: chartLines,
    );
  }

  static String _buildChordLine(List<ChordData> chords, double startBeat, double endBeat, 
                               int beatsPerMeasure, double charsPerBeat, int startMeasure) {
    int lineLength = ((endBeat - startBeat) * charsPerBeat).round();
    List<String> chordLine = List.filled(lineLength, ' ');

    for (var chord in chords) {
      if (chord.startBeat >= startBeat && chord.startBeat < endBeat) {
        double beatPos = chord.startBeat - startBeat;
        int charPos = (beatPos * charsPerBeat).round();
        
        // Limpiar espacio para el acorde
        for (int i = 0; i < chord.simplifiedChord.length && charPos + i < lineLength; i++) {
          chordLine[charPos + i] = ' ';
        }
        
        // Colocar el acorde
        for (int i = 0; i < chord.simplifiedChord.length && charPos + i < lineLength; i++) {
          chordLine[charPos + i] = chord.simplifiedChord[i];
        }
      }
    }

    return chordLine.join('');
  }

  static String _buildBarLine(int startMeasure, int endMeasure, int beatsPerMeasure, double charsPerBeat) {
    int lineLength = ((endMeasure - startMeasure) * beatsPerMeasure * charsPerBeat).round();
    List<String> barLine = List.filled(lineLength, '/');

    for (int m = startMeasure; m <= endMeasure; m++) {
      int beatPos = (m - startMeasure) * beatsPerMeasure;
      int charPos = (beatPos * charsPerBeat).round();
      if (charPos < lineLength) {
        barLine[charPos] = '|';
      }
    }

    return barLine.join('');
  }

  static String _buildMeasureLine(int startMeasure, int endMeasure, int beatsPerMeasure, double charsPerBeat) {
    int lineLength = ((endMeasure - startMeasure) * beatsPerMeasure * charsPerBeat).round();
    List<String> measureLine = List.filled(lineLength, ' ');

    for (int m = startMeasure; m < endMeasure; m++) {
      int beatPos = (m - startMeasure) * beatsPerMeasure;
      int charPos = (beatPos * charsPerBeat).round();
      String measureNum = (m + 1).toString();
      
      if (charPos < lineLength) {
        measureLine[charPos] = measureNum[0];
        if (measureNum.length > 1 && charPos + 1 < lineLength) {
          measureLine[charPos + 1] = measureNum[1];
        }
      }
    }

    return measureLine.join('');
  }
}