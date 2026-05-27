import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../widgets/add_allergy_form.dart';
import '../providers/allergy_provider.dart';
import '../../data/models/allergy_model.dart';

class AddAllergyScreen extends ConsumerWidget {
  const AddAllergyScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add Allergen'), centerTitle: false),
      body: AddAllergyForm(
        onSubmit: (name, reaction, severity) async {
          final isCritical = severity == AllergySeverity.severe || severity == AllergySeverity.anaphylactic;
          
          IconData icon;
          if (name.toLowerCase().contains('food') || name.toLowerCase().contains('peanut') || name.toLowerCase().contains('nut')) {
            icon = Icons.no_food;
          } else if (name.toLowerCase().contains('med') || name.toLowerCase().contains('penicillin') || name.toLowerCase().contains('drug')) {
            icon = Icons.medication;
          } else {
            icon = isCritical ? Icons.warning_amber_rounded : Icons.info_outline;
          }

          final newAllergy = AllergyModel(
            id: 'local_${DateTime.now().millisecondsSinceEpoch}',
            name: name,
            symptoms: reaction,
            severity: severity,
            isCritical: isCritical,
            icon: icon,
          );

          try {
            await ref.read(allergyRepositoryProvider).saveAllergy(newAllergy);
            
            // Refresh list
            ref.invalidate(allergiesProvider);

            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Successfully added allergy: $name'),
                duration: const Duration(seconds: 2),
              ),
            );
            Navigator.of(context).pop();
          } catch (e) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Failed to save allergy: $e'),
                duration: const Duration(seconds: 2),
              ),
            );
          }
        },
      ),
    );
  }
}
