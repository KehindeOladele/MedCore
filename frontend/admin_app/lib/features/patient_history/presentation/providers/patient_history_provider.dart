import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../data/models/medical_history_model.dart';
import '../../data/repositories/patient_history_repository.dart';

part 'patient_history_provider.g.dart';

@riverpod
PatientHistoryRepository patientHistoryRepository(Ref ref) {
  return PatientHistoryRepository();
}

@riverpod
Future<List<MedicalHistoryItem>> patientMedicalHistory(Ref ref) async {
  return ref.watch(patientHistoryRepositoryProvider).getMedicalHistory();
}
