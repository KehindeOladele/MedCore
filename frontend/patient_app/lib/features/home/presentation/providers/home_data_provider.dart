import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/material.dart';
import '../../../../features/history/data/models/medical_history_model.dart';
import '../../../../features/history/presentation/providers/history_provider.dart';
import '../../data/models/vital_model.dart';
import '../../data/models/activity_model.dart';
import '../../data/models/reminder_model.dart';
import '../../data/models/prescription_model.dart';
import '../../data/models/user_summary_model.dart';
import '../../data/repositories/home_repository.dart';
import '../../data/repositories/dashboard_repository.dart';
import 'home_controller.dart';
import '../../../profile/presentation/providers/menstrual_cycle_provider.dart';
import '../../../profile/presentation/providers/profile_provider.dart';
import '../../../../core/theme/app_colors.dart';

part 'home_data_provider.g.dart';

// ── Live backend provider ─────────────────────────────────────────────────────

/// Fetches the aggregated user summary from `GET /api/v1/user/summary`.
/// This is the primary source of truth for the home screen when online.
final userSummaryProvider = FutureProvider<UserSummaryModel>((ref) async {
  return DashboardRepository().getUserSummary();
});

@riverpod
HomeRepository homeRepository(Ref ref) {
  return HomeRepository();
}

@riverpod
Future<List<VitalModel>> vitals(Ref ref) async {
  final profileState = ref.watch(profileProvider);
  final fallbackIsFemale = ref.watch(genderProvider);
  final isFemale = profileState.maybeWhen(
    data: (profile) => profile.gender?.toLowerCase() == 'female',
    orElse: () => fallbackIsFemale,
  );
  final baseVitals = await ref
      .watch(homeRepositoryProvider)
      .getVitals(isFemale: isFemale);

  if (isFemale) {
    final cycle = await ref.watch(menstrualCycleProvider.future);
    if (cycle != null) {
      final difference = DateTime.now().difference(cycle.lastPeriodDate).inDays;
      var currentDay = difference + 1;
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

/// Maps the top 3 most recent MedicalHistoryItems from the live backend
/// into ActivityModel entries for the home screen activity feed.
@riverpod
Future<List<ActivityModel>> recentActivity(Ref ref) async {
  final historyAsync = ref.watch(historyProvider);

  return historyAsync.when(
    data: (items) {
      final recent = items.take(3).toList();

      return recent.map((item) {
        final IconData icon;
        final Color iconColor;
        final Color iconBg;

        switch (item.type) {
          case 'pharmacy':
            icon = Icons.local_pharmacy_outlined;
            iconColor = const Color(0xFF00BCD4);
            iconBg = const Color(0xFFE0F7FA);
            break;
          case 'lab':
            icon = Icons.science_outlined;
            iconColor = AppColors.blueAccent;
            iconBg = AppColors.blueBackground;
            break;
          case 'vaccine':
            icon = Icons.vaccines_outlined;
            iconColor = const Color(0xFF9C27B0);
            iconBg = const Color(0xFFF3E5F5);
            break;
          default: // diagnosis
            icon = Icons.monitor_heart_outlined;
            iconColor = AppColors.primary;
            iconBg = AppColors.primaryVariant;
        }

        const months = [
          'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
        ];
        final dateStr = '${months[item.date.month - 1]} ${item.date.day}';

        return ActivityModel(
          title: item.title,
          subtitle: item.subtitle,
          date: dateStr,
          icon: icon,
          iconColor: iconColor,
          iconBackgroundColor: iconBg,
        );
      }).toList();
    },
    loading: () => [],
    error: (_, __) => [],
  );
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
