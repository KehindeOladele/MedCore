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
      final response = await _apiService.get('/patients/me');
      final Map<String, dynamic> responseMap = Map<String, dynamic>.from(response as Map);
      
      // Merge local fhir_metadata cache if response fhir_metadata is empty/missing
      final cachedData = box.get(_cacheKey);
      if (cachedData != null) {
        try {
          final Map<String, dynamic> cachedMap = jsonDecode(cachedData) as Map<String, dynamic>;
          final cachedFhir = cachedMap['fhir_metadata'];
          final responseFhir = responseMap['fhir_metadata'];
          
          bool isResponseFhirEmpty = responseFhir == null || 
              (responseFhir is Map && (responseFhir.isEmpty || (responseFhir['resourceType'] == 'Patient' && responseFhir.length == 1)));
          
          if (cachedFhir != null && isResponseFhirEmpty) {
            responseMap['fhir_metadata'] = cachedFhir;
          }
        } catch (_) {
          // Ignore cache parsing errors and proceed
        }
      }
      
      // Save raw JSON to cache for offline access
      final jsonString = jsonEncode(responseMap);
      await box.put(_cacheKey, jsonString);

      return ProfileModel.fromJson(responseMap);
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
    final Map<String, dynamic> responseMap = Map<String, dynamic>.from(response as Map);
    
    // If response does not contain fhir_metadata, but payload did, merge it so it's cached locally
    if (!responseMap.containsKey('fhir_metadata') && payload.containsKey('fhir_metadata')) {
      responseMap['fhir_metadata'] = payload['fhir_metadata'];
    }
    
    // Update cache
    final jsonString = jsonEncode(responseMap);
    await box.put(_cacheKey, jsonString);
    
    return ProfileModel.fromJson(responseMap);
  }
}
