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
        iconBackgroundColor: AppColors.redBackground,
        backgroundColor: AppColors.redBackground,
        showChevron: true,
      ),
      VitalModel(
        title: "Set",
        subtitle: "Reminder",
        icon: Icons.medical_services_outlined,
        iconColor: Color(0xFF009688),
        iconBackgroundColor: Color(0xFFE0F2F1),
      ),
    ];
  }

  Future<List<ReminderModel>> getReminders() async {
    await Future.delayed(const Duration(milliseconds: 200));
    return [
      const ReminderModel(),
      // Adding a dummy second one to match UI placeholder if needed,
      // but UI handles the second item as a specific 'Add' button or placeholder
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
