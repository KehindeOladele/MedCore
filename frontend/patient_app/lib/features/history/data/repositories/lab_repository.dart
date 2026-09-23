import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/services/api_service.dart';
import '../models/lab_result_model.dart';

final labRepositoryProvider = Provider<LabRepository>((ref) {
  final api = ref.watch(apiServiceProvider);
  return LabRepository(api);
});

/// Provides the lab result for a specific lab ID.
/// Use [labResultProvider(labId)] to get an AsyncValue for the screen.
final labResultProvider =
    FutureProvider.family<LabResultModel, String>((ref, labId) async {
  final repo = ref.watch(labRepositoryProvider);
  return repo.fetchLabResult(labId);
});

class LabRepository {
  final ApiService _api;

  LabRepository(this._api);

  Future<LabResultModel> fetchLabResult(String labId) async {
    final data = await _api.get('/api/v1/lab-results/$labId');
    return LabResultModel.fromJson(Map<String, dynamic>.from(data as Map));
  }
}
