import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../features/history/data/models/medical_history_model.dart';
import '../../data/models/vital_model.dart';
import '../../data/models/activity_model.dart';
import '../../data/models/reminder_model.dart';
import '../../data/models/prescription_model.dart';
import '../../data/repositories/home_repository.dart';
import 'home_controller.dart';
import '../../../profile/presentation/providers/menstrual_cycle_provider.dart';

part 'home_data_provider.g.dart';

@riverpod
HomeRepository homeRepository(Ref ref) {
  return HomeRepository();
}

@riverpod
Future<List<VitalModel>> vitals(Ref ref) async {
  final isFemale = ref.watch(genderProvider);
  final baseVitals = await ref
      .watch(homeRepositoryProvider)
      .getVitals(isFemale: isFemale);

  if (isFemale) {
    final cycle = await ref.watch(menstrualCycleProvider.future);
    if (cycle != null) {
      final difference = DateTime.now().difference(cycle.lastPeriodDate).inDays;
      // Simple calculation: Day 1 is the start date.
      // If result is negative (future date), we might handle differently, but assuming past date:
      var currentDay = difference + 1;

      // If currentDay > cycleLength, it likely means a new cycle should have started or is late.
      // For visual simplicity in this MVP, we will show where they are relative to the logged start.
      // Or we could modulo if we assume regularity without logging: currentDay = (difference % cycle.cycleLength) + 1;
      // Let's stick to simple day count for now to encourage logging the new period.
      if (currentDay < 1) currentDay = 1;

      return baseVitals.map((v) {
        if (v.isFlow) {
          return VitalModel(
            title: v.title,
            subtitle: v.subtitle,
            icon: v.icon,
            iconColor: v.iconColor,
            iconBackgroundColor: v.iconBackgroundColor,
            isFlow: true,
            flowDay: currentDay,
            flowTotalDays: cycle.cycleLength,
          );
        }
        return v;
      }).toList();
    }
  }
  return baseVitals;
}

@riverpod
Future<List<ReminderModel>> reminders(Ref ref) async {
  return ref.watch(homeRepositoryProvider).getReminders();
}

@riverpod
Future<List<ActivityModel>> recentActivity(Ref ref) async {
  return ref.watch(homeRepositoryProvider).getRecentActivity();
}

@riverpod
Future<List<PrescriptionModel>> prescriptions(Ref ref) async {
  return ref.watch(homeRepositoryProvider).getPrescriptions();
}

final medicalHistoryProvider = FutureProvider<List<MedicalHistoryItem>>((
  ref,
) async {
  return ref.watch(homeRepositoryProvider).getMedicalHistory();
});
