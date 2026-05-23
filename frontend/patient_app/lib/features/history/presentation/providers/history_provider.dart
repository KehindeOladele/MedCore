import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/medical_history_model.dart';
import '../../data/repositories/history_repository.dart';

final historyProvider = AsyncNotifierProvider<HistoryNotifier, List<MedicalHistoryItem>>(() {
  return HistoryNotifier();
});

class HistoryNotifier extends AsyncNotifier<List<MedicalHistoryItem>> {
  late HistoryRepository _repository;

  @override
  Future<List<MedicalHistoryItem>> build() async {
    _repository = ref.watch(historyRepositoryProvider);
    return _fetchHistory();
  }

  Future<List<MedicalHistoryItem>> _fetchHistory() async {
    return await _repository.fetchMedicalHistory();
  }

  Future<void> refreshHistory() async {
    state = const AsyncValue.loading();
    try {
      final history = await _repository.fetchMedicalHistory();
      state = AsyncValue.data(history);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
