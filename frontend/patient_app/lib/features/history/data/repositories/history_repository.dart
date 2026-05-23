import 'dart:convert';
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

    try {
      final response = await _apiService.get('/api/v1/medical-history');
      
      // Response format: { "data": [ ... ] }
      final Map<String, dynamic> responseMap = response as Map<String, dynamic>;
      final List<dynamic> data = responseMap['data'] as List<dynamic>? ?? [];
      
      // Save raw JSON to cache for offline access
      final jsonString = jsonEncode(data);
      await box.put(_cacheKey, jsonString);

      return data.map((json) => MedicalHistoryItem.fromJson(json as Map<String, dynamic>)).toList();
    } catch (e) {
      // If network fails, attempt to load from cache
      final cachedData = box.get(_cacheKey);
      if (cachedData != null) {
        final decoded = jsonDecode(cachedData) as List<dynamic>;
        return decoded.map((json) => MedicalHistoryItem.fromJson(json as Map<String, dynamic>)).toList();
      }
      
      // If no cache exists, rethrow the original error
      rethrow;
    }
  }
}
