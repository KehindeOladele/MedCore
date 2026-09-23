import 'package:flutter/material.dart';

class MedicalRecordModel {
  final String title;
  final String subtitle;
  final String date;
  final String status; // 'Normal', 'Needs Review', etc.
  final String type; // 'lab', 'imaging', 'prescription'
  final String? iconPath;
  final Color? cardBackgroundColor;
  final Color? badgeColor;
  final Color? badgeTextColor;

  MedicalRecordModel({
    required this.title,
    required this.subtitle,
    required this.date,
    required this.status,
    required this.type,
    this.iconPath,
    this.cardBackgroundColor,
    this.badgeColor,
    this.badgeTextColor,
  });
}
