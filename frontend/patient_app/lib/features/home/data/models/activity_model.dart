import 'package:flutter/material.dart';

class ActivityModel {
  final String title;
  final String subtitle;
  final String date;
  final IconData icon;
  final Color iconColor;
  final Color iconBackgroundColor;

  const ActivityModel({
    required this.title,
    required this.subtitle,
    required this.date,
    required this.icon,
    required this.iconColor,
    required this.iconBackgroundColor,
  });
}
