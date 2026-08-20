import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../data/models/patient_models.dart';
import '../../data/repositories/patient_repository.dart';

part 'patient_controller.g.dart';

// State: null = no search yet, [] = searched but no results, [...]  = results
@riverpod
class PatientController extends _$PatientController {
  @override
  AsyncValue<List<Patient>?> build() {
    // Start with null = idle, no search has been made
    return const AsyncValue.data(null);
  }

  Future<void> search(String query) async {
    if (query.trim().isEmpty) {
      // User cleared the search — go back to idle state
      state = const AsyncValue.data(null);
      return;
    }

    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.read(patientRepositoryProvider);
      final all = await repository.getMyPatients();
      // Filter locally by name or ID
      final q = query.trim().toLowerCase();
      return all.where((p) {
        return p.fullName.toLowerCase().contains(q) ||
            p.id.toLowerCase().contains(q);
      }).toList();
    });
  }

  void reset() {
    state = const AsyncValue.data(null);
  }
}
