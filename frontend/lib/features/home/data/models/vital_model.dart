import 'package:flutter/material.dart';

class VitalModel {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color iconColor;
  final Color iconBackgroundColor;
  final Color? backgroundColor;
  final bool showChevron;

  const VitalModel({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.iconColor,
    required this.iconBackgroundColor,
    this.backgroundColor,
    this.showChevron = false,
  });
}
