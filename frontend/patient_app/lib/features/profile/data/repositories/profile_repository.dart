import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/services/api_service.dart';
import '../models/profile_model.dart';

final profileRepositoryProvider = Provider<ProfileRepository>((ref) {
  final apiService = ref.watch(apiServiceProvider);
  return ProfileRepository(apiService);
});

class ProfileRepository {
  final ApiService _apiService;
  static const String _boxName = 'profile_cache';
  static const String _cacheKey = 'my_profile';

  ProfileRepository(this._apiService);

  Future<Box<String>> _getBox() async {
    if (!Hive.isBoxOpen(_boxName)) {
      return await Hive.openBox<String>(_boxName);
    }
    return Hive.box<String>(_boxName);
  }

  Future<ProfileModel> fetchProfile() async {
    final box = await _getBox();

    try {
      final response = await _apiService.get('/patients/profile/me');
      
      // Save raw JSON to cache for offline access
      final jsonString = jsonEncode(response);
      await box.put(_cacheKey, jsonString);

      return ProfileModel.fromJson(response as Map<String, dynamic>);
    } catch (e) {
      // If network fails, attempt to load from cache
      final cachedData = box.get(_cacheKey);
      if (cachedData != null) {
        final decoded = jsonDecode(cachedData);
        return ProfileModel.fromJson(decoded as Map<String, dynamic>);
      }
      
      // If no cache exists, rethrow the original error
      rethrow;
    }
  }

  Future<ProfileModel> updateProfile(Map<String, dynamic> payload) async {
    final box = await _getBox();
    
    // Attempt network request
    final response = await _apiService.put('/patients/profile/me', payload);
    
    // Update cache
    final jsonString = jsonEncode(response);
    await box.put(_cacheKey, jsonString);
    
    return ProfileModel.fromJson(response as Map<String, dynamic>);
  }
}
