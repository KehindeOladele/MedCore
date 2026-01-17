import 'package:flutter/material.dart';

class PrescriptionModel {
  final String title;
  final String subtitle;
  final String dosage;
  final String schedule; // e.g. "3 times daily (Every 8 hours)"
  final IconData icon;
  final Color iconColor;
  final Color iconBackgroundColor;
  final Color? badgeColor; // For the dosage badge logic if needed
  final Color? backgroundColor;

  const PrescriptionModel({
    required this.title,
    required this.subtitle,
    required this.dosage,
    required this.schedule,
    required this.icon,
    this.iconColor = const Color(0xFF009688), // Default Green
    this.iconBackgroundColor = const Color(0xFFE0F2F1), // Default Light Green
    this.badgeColor,
    this.backgroundColor,
  });
}
