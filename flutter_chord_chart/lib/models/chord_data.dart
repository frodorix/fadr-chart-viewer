class ChordData {
  final String chord;
  final double start;
  final double end;
  late double startBeat;
  late double endBeat;
  late String simplifiedChord;

  ChordData({
    required this.chord,
    required this.start,
    required this.end,
  }) {
    simplifiedChord = _simplifyChord(chord);
  }

  String _simplifyChord(String chord) {
    if (chord.contains(':maj')) {
      return chord.replaceAll(':maj', '');
    } else if (chord.contains(':min')) {
      return chord.replaceAll(':min', 'm');
    }
    return chord;
  }

  void calculateBeats(double bpm) {
    startBeat = start * (bpm / 60.0);
    endBeat = end * (bpm / 60.0);
  }

  factory ChordData.fromCsvRow(List<dynamic> row) {
    return ChordData(
      chord: row[0].toString(),
      start: double.parse(row[1].toString()),
      end: double.parse(row[2].toString()),
    );
  }
}