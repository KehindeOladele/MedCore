import 'package:flutter/material.dart';
import 'package:hive/hive.dart';

class ReminderModel extends HiveObject {
  // Placeholder for now as the UI uses a widget mostly
  // But strictly, we might want:
  @HiveField(0)
  String title;
  @HiveField(1)
  String subtitle;
  @HiveField(2)
  String tagText;
  @HiveField(3)
  Color tagColor;
  @HiveField(4)
  IconData icon;
  @HiveField(5)
  String? imageUrl;
  @HiveField(6)
  String time;
  @HiveField(7)
  bool isCompleted;
  @HiveField(8)
  bool isMissed;
  @HiveField(9)
  bool isUrgent;

  ReminderModel({
    required this.title,
    required this.subtitle,
    required this.tagText,
    required this.tagColor,
    required this.icon,
    required this.time,
    this.imageUrl,
    this.isCompleted = false,
    this.isMissed = false,
    this.isUrgent = false,
  });
}
