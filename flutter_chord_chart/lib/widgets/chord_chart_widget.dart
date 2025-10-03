import 'package:flutter/material.dart';
import '../models/chord_data.dart';

class ChordChartPainter extends CustomPainter {
  final List<ChordData> chords;
  final double bpm;
  final int beatsPerMeasure;
  final int measuresPerLine;
  final double charsPerBeat;

  ChordChartPainter({
    required this.chords,
    required this.bpm,
    required this.beatsPerMeasure,
    required this.measuresPerLine,
    required this.charsPerBeat,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (chords.isEmpty) return;

    // Calcular beats para todos los acordes
    for (var chord in chords) {
      chord.calculateBeats(bpm);
    }

    final paint = Paint()
      ..color = Colors.black
      ..strokeWidth = 1.0;

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    // Configuración de diseño
    const double lineHeight = 80.0;
    const double chordLineOffset = 20.0;
    const double barLineOffset = 40.0;
    const double measureLineOffset = 60.0;
    
    double charWidth = size.width / (measuresPerLine * beatsPerMeasure * charsPerBeat);
    
    // Calcular total de medidas
    double maxBeat = chords.map((c) => c.endBeat).reduce((a, b) => a > b ? a : b);
    int totalMeasures = (maxBeat / beatsPerMeasure).ceil();

    int currentMeasure = 0;
    double currentY = 40.0;

    while (currentMeasure < totalMeasures && currentY < size.height - lineHeight) {
      int startMeasure = currentMeasure;
      int endMeasure = (startMeasure + measuresPerLine).clamp(0, totalMeasures);
      
      double startBeat = startMeasure * beatsPerMeasure.toDouble();
      double endBeat = endMeasure * beatsPerMeasure.toDouble();
      
      // Dibujar líneas de compás
      for (int m = startMeasure; m <= endMeasure; m++) {
        double beatPos = (m - startMeasure) * beatsPerMeasure.toDouble();
        double xPos = beatPos * charsPerBeat * charWidth;
        
        if (xPos <= size.width) {
          // Línea vertical de compás
          canvas.drawLine(
            Offset(xPos, currentY + barLineOffset - 5),
            Offset(xPos, currentY + barLineOffset + 5),
            paint,
          );
          
          // Número de compás
          if (m < totalMeasures) {
            textPainter.text = TextSpan(
              text: '${m + 1}',
              style: const TextStyle(
                fontSize: 12,
                color: Colors.black,
                fontFamily: 'monospace',
              ),
            );
            textPainter.layout();
            textPainter.paint(canvas, Offset(xPos + 2, currentY + measureLineOffset));
          }
        }
      }
      
      // Dibujar línea de barras (slashes)
      double lineWidth = (endMeasure - startMeasure) * beatsPerMeasure * charsPerBeat * charWidth;
      for (double x = 0; x < lineWidth; x += charWidth * 2) {
        if (x < size.width) {
          // Dibujar slash
          canvas.drawLine(
            Offset(x, currentY + barLineOffset - 3),
            Offset(x + charWidth, currentY + barLineOffset + 3),
            paint,
          );
        }
      }
      
      // Dibujar acordes
      for (var chord in chords) {
        if (chord.startBeat >= startBeat && chord.startBeat < endBeat) {
          double beatPos = chord.startBeat - startBeat;
          double xPos = beatPos * charsPerBeat * charWidth;
          
          if (xPos < size.width) {
            textPainter.text = TextSpan(
              text: chord.simplifiedChord,
              style: const TextStyle(
                fontSize: 14,
                color: Colors.black,
                fontWeight: FontWeight.bold,
                fontFamily: 'monospace',
              ),
            );
            textPainter.layout();
            textPainter.paint(canvas, Offset(xPos, currentY + chordLineOffset));
          }
        }
      }
      
      currentMeasure = endMeasure;
      currentY += lineHeight;
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => true;
}

class ChordChartWidget extends StatelessWidget {
  final List<ChordData> chords;
  final double bpm;
  final int beatsPerMeasure;
  final int measuresPerLine;
  final double charsPerBeat;

  const ChordChartWidget({
    Key? key,
    required this.chords,
    required this.bpm,
    required this.beatsPerMeasure,
    required this.measuresPerLine,
    required this.charsPerBeat,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
        color: Colors.white,
      ),
      child: CustomPaint(
        painter: ChordChartPainter(
          chords: chords,
          bpm: bpm,
          beatsPerMeasure: beatsPerMeasure,
          measuresPerLine: measuresPerLine,
          charsPerBeat: charsPerBeat,
        ),
        size: Size.infinite,
      ),
    );
  }
}