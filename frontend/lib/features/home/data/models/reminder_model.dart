import 'package:flutter/material.dart';

class ReminderModel {
  // Placeholder for now as the UI uses a widget mostly
  // But strictly, we might want:
  final String title;
  final String subtitle;
  final String tagText;
  final Color tagColor;
  final IconData icon;
  final String? imageUrl;

  const ReminderModel({
    required this.title,
    required this.subtitle,
    required this.tagText,
    required this.tagColor,
    required this.icon,
    this.imageUrl,
  });
}
