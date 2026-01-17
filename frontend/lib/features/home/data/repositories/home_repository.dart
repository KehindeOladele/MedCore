import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../models/vital_model.dart';
import '../models/activity_model.dart';
import '../models/reminder_model.dart';

class HomeRepository {
  Future<List<VitalModel>> getVitals() async {
    // Simulate API delay
    await Future.delayed(const Duration(milliseconds: 200));

    return const [
      VitalModel(
        title: "A+",
        subtitle: "Blood Group",
        icon: Icons.water_drop_outlined,
        iconColor: AppColors.primary,
        iconBackgroundColor: AppColors.primaryVariant,
      ),
      VitalModel(
        title: "AA",
        subtitle: "Genotype",
        icon: Icons.fingerprint,
        iconColor: Colors.grey,
        iconBackgroundColor: Color(0xFFF5F5F5),
      ),
      VitalModel(
        title: "Penicillin",
        subtitle: "Allergies",
        icon: Icons.warning_amber_rounded,
        iconColor: AppColors.redAccent,
        iconBackgroundColor: Colors.white, // White circle on red card
        backgroundColor: AppColors.redBackground,
        showChevron: true,
        titleColor: AppColors.redAccent,
      ),
      VitalModel(
        title: "Set",
        subtitle: "Reminder",
        icon: Icons.medical_services_outlined,
        iconColor: Color(0xFF009688),
        iconBackgroundColor: Colors.white, // White circle on green card
        backgroundColor: Color(0xFFE0F2F1),
        titleColor: Color(0xFF009688),
      ),
    ];
  }

  Future<List<ReminderModel>> getReminders() async {
    await Future.delayed(const Duration(milliseconds: 200));
    return [
      ReminderModel(
        title: "Cardiology Checkup",
        subtitle: "Dr. Ozioma • 10:00 AM",
        tagText: "Tomorrow",
        tagColor: AppColors.primary,
        icon: Icons.monitor_heart,
        imageUrl: 'https://i.pravatar.cc/150?img=5',
      ),
      ReminderModel(
        title: "Take Vitamins",
        subtitle: "With Lunch • 12:30 PM",
        tagText: "Daily",
        tagColor: Colors.orange,
        icon: Icons.medication,
      ),
      ReminderModel(
        title: "Lab Results",
        subtitle: "Blood test view",
        tagText: "New",
        tagColor: Colors.purple,
        icon: Icons.science,
      ),
    ];
  }

  Future<List<ActivityModel>> getRecentActivity() async {
    await Future.delayed(const Duration(milliseconds: 200));
    return const [
      ActivityModel(
        title: "General Checkup",
        subtitle: "General Hospital • Dr. Isreal",
        date: "Oct 24",
        icon: Icons.monitor_heart,
        iconColor: AppColors.primary,
        iconBackgroundColor: AppColors.primaryVariant,
      ),
      ActivityModel(
        title: "Blood Test Results",
        subtitle: "Lab Corp • Complete Panel",
        date: "Oct 20",
        icon: Icons.water_drop,
        iconColor: Color(0xFF009688),
        iconBackgroundColor: Color(0xFFE0F2F1),
      ),
      ActivityModel(
        title: "Flu Vaccination",
        subtitle: "Garki Clinic",
        date: "Sep 15",
        icon: Icons.vaccines,
        iconColor: AppColors.blueAccent,
        iconBackgroundColor: AppColors.blueBackground,
      ),
    ];
  }
}
