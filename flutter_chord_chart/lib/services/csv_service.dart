import 'dart:io';
import 'package:csv/csv.dart';
import 'package:file_picker/file_picker.dart';
import '../models/chord_data.dart';

class CsvService {
  static Future<List<ChordData>?> loadChordDataFromFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['csv'],
      );

      if (result != null) {
        File file = File(result.files.single.path!);
        return await loadChordDataFromPath(file.path);
      }
      return null;
    } catch (e) {
      print('Error al cargar archivo CSV: $e');
      return null;
    }
  }

  static Future<List<ChordData>> loadChordDataFromPath(String filePath) async {
    try {
      final file = File(filePath);
      final contents = await file.readAsString();
      List<List<dynamic>> csvData = const CsvToListConverter().convert(contents);
      
      // Omitir la primera fila (headers)
      List<ChordData> chords = [];
      for (int i = 1; i < csvData.length; i++) {
        if (csvData[i].length >= 3) {
          chords.add(ChordData.fromCsvRow(csvData[i]));
        }
      }
      
      return chords;
    } catch (e) {
      print('Error al procesar CSV: $e');
      return [];
    }
  }

  static List<ChordData> loadChordDataFromString(String csvContent) {
    try {
      List<List<dynamic>> csvData = const CsvToListConverter().convert(csvContent);
      
      List<ChordData> chords = [];
      for (int i = 1; i < csvData.length; i++) {
        if (csvData[i].length >= 3) {
          chords.add(ChordData.fromCsvRow(csvData[i]));
        }
      }
      
      return chords;
    } catch (e) {
      print('Error al procesar CSV: $e');
      return [];
    }
  }
}