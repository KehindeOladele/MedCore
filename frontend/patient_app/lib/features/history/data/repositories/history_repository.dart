import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/services/api_service.dart';
import '../models/medical_history_model.dart';

final historyRepositoryProvider = Provider<HistoryRepository>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return HistoryRepository(apiService);
});

class HistoryRepository {
  final ApiService _apiService;
  static const String _boxName = 'history_cache';
  static const String _cacheKey = 'my_history';

  HistoryRepository(this._apiService);

  Future<Box<String>> _getBox() async {
    if (!Hive.isBoxOpen(_boxName)) {
      return await Hive.openBox<String>(_boxName);
    }
    return Hive.box<String>(_boxName);
  }

  Future<List<MedicalHistoryItem>> fetchMedicalHistory() async {
    final box = await _getBox();
    List<MedicalHistoryItem> backendItems = [];

    try {
      final response = await _apiService.get('/api/v1/medical-history');
      
      // Response format: { "data": [ ... ] }
      final Map<String, dynamic> responseMap = response as Map<String, dynamic>;
      final List<dynamic> data = responseMap['data'] as List<dynamic>? ?? [];
      
      // Save raw JSON to cache for offline access
      final jsonString = jsonEncode(data);
      await box.put(_cacheKey, jsonString);

      backendItems = data.map((json) => MedicalHistoryItem.fromJson(json as Map<String, dynamic>)).toList();
    } catch (e) {
      // If network fails, attempt to load from cache
      final cachedData = box.get(_cacheKey);
      if (cachedData != null) {
        final decoded = jsonDecode(cachedData) as List<dynamic>;
        backendItems = decoded.map((json) => MedicalHistoryItem.fromJson(json as Map<String, dynamic>)).toList();
      } else {
        // If there's no cache and network fails, print error and proceed with empty backend list
        debugPrint('Error fetching medical history: $e');
      }
    }

    // Get local medical history items
    final localBox = Hive.box<MedicalHistoryItem>('local_history');
    final List<MedicalHistoryItem> localItems = localBox.values.toList();

    // Merge backend items and local items
    final allItems = [...backendItems, ...localItems];

    // Sort chronologically descending (newest first)
    allItems.sort((a, b) => b.date.compareTo(a.date));

    return allItems;
  }

  Future<void> addLocalMedicalHistory(MedicalHistoryItem item) async {
    final localBox = Hive.box<MedicalHistoryItem>('local_history');
    await localBox.add(item);
  }
}
