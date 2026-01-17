import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../data/repositories/home_repository.dart';
import '../../data/models/vital_model.dart';
import '../../data/models/activity_model.dart';
import '../../data/models/reminder_model.dart';
import '../../data/models/prescription_model.dart';
import '../../data/repositories/home_repository.dart';

part 'home_data_provider.g.dart';

@riverpod
HomeRepository homeRepository(Ref ref) {
  return HomeRepository();
}

@riverpod
Future<List<VitalModel>> vitals(Ref ref) async {
  return ref.watch(homeRepositoryProvider).getVitals();
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
