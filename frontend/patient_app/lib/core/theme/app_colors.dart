import 'package:flutter/material.dart';

class AppColors {
  // Primary (shared across both)
  static const Color primary = Color(0xFF00C853); // Vitals Green
  static const Color primaryVariant = Color(0xFFE8F5E9);

  // --- Light Mode ---
  static const Color backgroundLight = Color(0xFFF5F5F5);
  static const Color surfaceLight = Colors.white;
  static const Color textPrimaryLight = Color(0xFF1A1A1A);
  static const Color textSecondaryLight = Color(0xFF757575);

  // --- Dark Mode ---
  static const Color backgroundDark = Color(0xFF121212);
  static const Color surfaceDark = Color(0xFF1E1E1E);
  static const Color textPrimaryDark = Color(0xFFE0E0E0);
  static const Color textSecondaryDark = Color(0xFFAAAAAA);

  // Status/Accents
  static const Color redAccent = Color(0xFFFF5252);
  static const Color redBackground = Color(0xFFFFEBEE);
  static const Color blueAccent = Color(0xFF448AFF);
  static const Color blueBackground = Color(0xFFE3F2FD);
  static const Color orangeAccent = Color(0xFFFFAB40);
  static const Color orangeBackground = Color(0xFFFFF3E0);

  // To prevent breaking existing hardcoded values during transition, we keep legacy getters
  static const Color background = backgroundLight;
  static const Color surface = surfaceLight;
  static const Color textPrimary = textPrimaryLight;
  static const Color textSecondary = textSecondaryLight;
}
