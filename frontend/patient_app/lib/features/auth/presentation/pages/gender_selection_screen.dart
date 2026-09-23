import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:medcore/features/home/presentation/providers/home_controller.dart';

class GenderSelectionScreen extends ConsumerWidget {
  const GenderSelectionScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          child: Column(
            children: [
              const SizedBox(height: 32),
              // MedCore title
              const Text(
                'MedCore',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF059669),
                ),
              ),
              const SizedBox(height: 20),
              // Medical cross icon
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: const Color(0xFF059669).withOpacity(0.1),
                ),
                child: const Center(
                  child: Icon(
                    Icons.add_circle_outline,
                    color: Color(0xFF059669),
                    size: 40,
                  ),
                ),
              ),
              const SizedBox(height: 48),
              // Help text
              const Text(
                'Tell us your gender',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  color: Color(0xFF191919),
                ),
              ),
              const SizedBox(height: 32),
              // Gender buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Male button
                  Expanded(
                    child: _buildGenderButton(
                      context,
                      ref,
                      icon: Icons.male,
                      label: 'Male',
                      isFemale: false,
                    ),
                  ),
                  const SizedBox(width: 16),
                  // Female button
                  Expanded(
                    child: _buildGenderButton(
                      context,
                      ref,
                      icon: Icons.female,
                      label: 'Female',
                      isFemale: true,
                    ),
                  ),
                ],
              ),
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGenderButton(
    BuildContext context,
    WidgetRef ref, {
    required IconData icon,
    required String label,
    required bool isFemale,
  }) {
    return GestureDetector(
      onTap: () {
        ref.read(genderProvider.notifier).setGender(isFemale);
        Navigator.of(context).pushReplacementNamed('/patient_login');
      },
      child: Container(
        height: 140,
        decoration: BoxDecoration(
          border: Border.all(
            color: const Color(0xFF059669),
            width: 2,
          ),
          borderRadius: BorderRadius.circular(16),
          color: Colors.white,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              color: const Color(0xFF059669),
              size: 48,
            ),
            const SizedBox(height: 12),
            Text(
              label,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: Color(0xFF191919),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
