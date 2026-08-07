import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../data/models/menstrual_cycle_model.dart';
import '../../data/repositories/menstrual_cycle_repository.dart';

part 'menstrual_cycle_provider.g.dart';

@riverpod
MenstrualCycleRepository menstrualCycleRepository(Ref ref) {
  return MenstrualCycleRepository();
}

@riverpod
class MenstrualCycle extends _$MenstrualCycle {
  @override
  Future<MenstrualCycleModel?> build() async {
    final repository = ref.read(menstrualCycleRepositoryProvider);
    return repository.getCycle();
  }

  Future<void> saveCycle(MenstrualCycleModel cycle) async {
    state = const AsyncValue.loading();
    try {
      final repository = ref.read(menstrualCycleRepositoryProvider);
      await repository.saveCycle(cycle);
      state = AsyncValue.data(cycle);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
