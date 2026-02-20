import 'package:flutter/material.dart';
import '../widgets/add_allergy_form.dart';

class AddAllergyScreen extends StatelessWidget {
  const AddAllergyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add Allergen'), centerTitle: false),
      body: AddAllergyForm(
        onSubmit: (name, reaction, severity) {
          // TODO: Handle form submission - save to database via provider
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Added allergy: $name'),
              duration: const Duration(seconds: 2),
            ),
          );
          Navigator.of(context).pop();
        },
      ),
    );
  }
}
