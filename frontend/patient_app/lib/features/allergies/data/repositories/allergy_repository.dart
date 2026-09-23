import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../home/presentation/providers/home_data_provider.dart';
import '../../../profile/data/repositories/profile_repository.dart';
import '../models/allergy_model.dart';

class AllergyRepository {
  final Ref _ref;

  AllergyRepository(this._ref);

  Future<List<AllergyModel>> getAllergies() async {
    List<String> backendAllergyNames = [];

    // 1. Attempt to fetch backend allergies from the live summary provider
    try {
      final summary = await _ref.read(userSummaryProvider.future);
      backendAllergyNames = summary.vitals.allergies;
    } catch (_) {
      // Fallback: offline or not loaded yet.
    }

    // 2. Fetch locally stored patient allergies from Hive
    final box = Hive.box<AllergyModel>('local_allergies');
    final localAllergies = box.values.toList();

    // 3. Map backend strings to the detailed AllergyModel structures
    final mappedBackendAllergies = backendAllergyNames.map((name) {
      return _mapStringToAllergyModel(name);
    }).toList();

    // 4. Merge lists, removing duplicates by name (case-insensitive)
    final allAllergies = <AllergyModel>[];
    final seenNames = <String>{};

    for (var allergy in mappedBackendAllergies) {
      if (seenNames.add(allergy.name.toLowerCase())) {
        allAllergies.add(allergy);
      }
    }
    for (var allergy in localAllergies) {
      if (seenNames.add(allergy.name.toLowerCase())) {
        allAllergies.add(allergy);
      }
    }

    return allAllergies;
  }

  /// Saves the allergy locally AND syncs the full allergy list to the backend
  /// by merging it into the patient's fhir_metadata via PUT /patients/profile/me.
  Future<void> saveAllergy(AllergyModel allergy) async {
    // 1. Save to local Hive first
    final box = Hive.box<AllergyModel>('local_allergies');
    await box.put(allergy.id, allergy);

    // 2. Collect all allergy names (local + new) for backend sync
    try {
      final allAllergies = await getAllergies();
      final allergyNames = allAllergies.map((a) => a.name).toList();

      final profileRepo = _ref.read(profileRepositoryProvider);
      // Fetch current profile to preserve existing fhir_metadata fields
      final currentProfile = await profileRepo.fetchProfile();
      final updatedFhir = Map<String, dynamic>.from(currentProfile.fhirMetadata)
        ..['allergies'] = allergyNames;

      await profileRepo.updateProfile({'fhir_metadata': updatedFhir});
    } catch (_) {
      // Backend sync is best-effort; local save already succeeded
    }
  }

  AllergyModel _mapStringToAllergyModel(String name) {
    final lowerName = name.toLowerCase();
    if (lowerName.contains('penicillin')) {
      return AllergyModel(
        id: 'backend_penicillin',
        name: 'Penicillin',
        symptoms: 'Severe rash, shortness of breath',
        severity: AllergySeverity.severe,
        isCritical: true,
        icon: Icons.medication,
      );
    } else if (lowerName.contains('peanut')) {
      return AllergyModel(
        id: 'backend_peanuts',
        name: 'Peanuts',
        symptoms: 'Airways swelling, hives',
        severity: AllergySeverity.anaphylactic,
        isCritical: true,
        icon: Icons.no_food,
      );
    } else if (lowerName.contains('pollen')) {
      return AllergyModel(
        id: 'backend_pollen',
        name: 'Pollen',
        symptoms: 'Seasonal Rhinitis',
        severity: AllergySeverity.moderate,
        isCritical: false,
        icon: Icons.filter_vintage,
      );
    } else if (lowerName.contains('latex')) {
      return AllergyModel(
        id: 'backend_latex',
        name: 'Latex',
        symptoms: 'Contact Dermatitis',
        severity: AllergySeverity.mild,
        isCritical: false,
        icon: Icons.masks,
      );
    } else if (lowerName.contains('pet dander') || lowerName.contains('cat') || lowerName.contains('dog')) {
      return AllergyModel(
        id: 'backend_pet_dander',
        name: name,
        symptoms: 'Sneezing, watery eyes',
        severity: AllergySeverity.mild,
        isCritical: false,
        icon: Icons.cruelty_free,
      );
    }

    // Default mapping for other allergen strings from backend
    return AllergyModel(
      id: 'backend_${name.hashCode}',
      name: name,
      symptoms: 'Unknown reaction details',
      severity: AllergySeverity.moderate,
      isCritical: false,
      icon: Icons.warning_amber_rounded,
    );
  }
}
