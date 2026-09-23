import 'package:flutter/material.dart';

enum AllergySeverity { anaphylactic, severe, moderate, mild }

class AllergyModel {
  final String id;
  final String name;
  final String symptoms;
  final AllergySeverity severity;
  final bool isCritical;
  final IconData? icon;
  final String? assetPath;

  const AllergyModel({
    required this.id,
    required this.name,
    required this.symptoms,
    required this.severity,
    this.isCritical = false,
    this.icon,
    this.assetPath,
  });
}
