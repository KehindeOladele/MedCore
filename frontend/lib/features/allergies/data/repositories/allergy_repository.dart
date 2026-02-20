import 'package:flutter/material.dart';
import '../models/allergy_model.dart';

class AllergyRepository {
  Future<List<AllergyModel>> getAllergies() async {
    // Simulate API delay
    await Future.delayed(const Duration(milliseconds: 200));

    return const [
      // Critical
      AllergyModel(
        id: '1',
        name: 'Peanuts',
        symptoms: 'Airways swelling, hives',
        severity: AllergySeverity.anaphylactic,
        isCritical: true,
        icon: Icons.no_food,
      ),
      AllergyModel(
        id: '2',
        name: 'Penicillin',
        symptoms: 'Severe rash, shortness of breath',
        severity: AllergySeverity.severe,
        isCritical: true,
        icon: Icons.medication,
      ),
      // Other
      AllergyModel(
        id: '3',
        name: 'Pollen',
        symptoms: 'Seasonal Rhinitis',
        severity: AllergySeverity.moderate,
        isCritical: false,
        icon: Icons.coronavirus,
      ),
      AllergyModel(
        id: '4',
        name: 'Latex',
        symptoms: 'Contact Dermatitis',
        severity: AllergySeverity.mild,
        isCritical: false,
        icon: Icons.masks,
      ),
      AllergyModel(
        id: '5',
        name: 'Pet Dander',
        symptoms: 'Sneezing, watery eyes',
        severity: AllergySeverity.mild,
        isCritical: false,
        icon: Icons.cruelty_free, // Approximating rabbit/pet icon
      ),
    ];
  }
}
