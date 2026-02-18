import 'package:flutter/material.dart';

class VitalModel {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color iconColor;
  final Color iconBackgroundColor;
  final Color? backgroundColor;
  final bool showChevron;

  final bool isFlow;
  final int? flowDay;
  final int? flowTotalDays;

  const VitalModel({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.iconColor,
    required this.iconBackgroundColor,
    this.backgroundColor,
    this.showChevron = false,
    this.titleColor,
    this.isFlow = false,
    this.flowDay,
    this.flowTotalDays,
    this.secondaryTitle,
    this.secondarySubtitle,
  });

  final Color? titleColor;
  final String? secondaryTitle;
  final String? secondarySubtitle;
}
