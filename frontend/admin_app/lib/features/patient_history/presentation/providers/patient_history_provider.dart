import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../data/models/medical_history_model.dart';
import '../../data/repositories/patient_history_repository.dart';

part 'patient_history_provider.g.dart';

@riverpod
PatientHistoryRepository patientHistoryRepository(Ref ref) {
  return PatientHistoryRepository.instance;
}

@riverpod
Future<List<MedicalHistoryItem>> patientMedicalHistory(Ref ref) async {
  final repo = ref.watch(patientHistoryRepositoryProvider);

  // Re-run this provider whenever the history ValueNotifier changes
  void listener() => ref.invalidateSelf();
  repo.history.addListener(listener);
  ref.onDispose(() => repo.history.removeListener(listener));

  return repo.getMedicalHistory();
}
