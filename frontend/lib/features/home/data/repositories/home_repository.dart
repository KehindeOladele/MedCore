import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../../../../core/theme/app_colors.dart';
import '../models/vital_model.dart';
import '../models/activity_model.dart';
import '../models/reminder_model.dart';
import '../models/prescription_model.dart';

class HomeRepository {
  Future<List<PrescriptionModel>> getPrescriptions() async {
    final box = Hive.box<PrescriptionModel>('prescriptions');
    return box.values.toList();
  }

  Future<void> addPrescription(PrescriptionModel prescription) async {
    final box = Hive.box<PrescriptionModel>('prescriptions');
    await box.add(prescription);
  }

  Future<List<VitalModel>> getVitals({bool isFemale = false}) async {
    // Simulate API delay
    await Future.delayed(const Duration(milliseconds: 200));

    if (isFemale) {
      return const [
        VitalModel(
          title: "O+",
          subtitle: "Blood Group",
          icon: Icons.water_drop_outlined,
          iconColor: AppColors.primary,
          iconBackgroundColor: AppColors.primaryVariant,
          secondaryTitle: "AA",
          secondarySubtitle: "Genotype",
        ),
        VitalModel(
          title: "Flow",
          subtitle: "Flow",
          icon: Icons.water_drop,
          iconColor: Colors.red,
          iconBackgroundColor: Colors.red,
          isFlow: true,
          flowDay: 20,
          flowTotalDays: 28,
        ),
        VitalModel(
          title: "Penicillin",
          subtitle: "Allergies",
          icon: Icons.warning_amber_rounded,
          iconColor: AppColors.redAccent,
          iconBackgroundColor: Colors.white,
          backgroundColor: AppColors.redBackground,
          showChevron: true,
          titleColor: AppColors.redAccent,
        ),
        VitalModel(
          title: "Set",
          subtitle: "Reminder",
          icon: Icons.medical_services_outlined,
          iconColor: Color(0xFF009688),
          iconBackgroundColor: Colors.white,
          backgroundColor: Color(0xFFE0F2F1),
          titleColor: Color(0xFF009688),
        ),
      ];
    }

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
        iconBackgroundColor: Colors.white,
        backgroundColor: AppColors.redBackground,
        showChevron: true,
        titleColor: AppColors.redAccent,
      ),
      VitalModel(
        title: "Set",
        subtitle: "Reminder",
        icon: Icons.medical_services_outlined,
        iconColor: Color(0xFF009688),
        iconBackgroundColor: Colors.white,
        backgroundColor: Color(0xFFE0F2F1),
        titleColor: Color(0xFF009688),
      ),
    ];
  }

  Future<List<ReminderModel>> getReminders() async {
    final box = Hive.box<ReminderModel>('reminders');
    return box.values.toList();
  }

  Future<void> addReminder(ReminderModel reminder) async {
    final box = Hive.box<ReminderModel>('reminders');
    await box.add(reminder);
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
