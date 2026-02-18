import 'package:hive_flutter/hive_flutter.dart';
import '../models/menstrual_cycle_model.dart';

class MenstrualCycleRepository {
  static const String boxName = 'menstrual_cycles';

  Future<void> saveCycle(MenstrualCycleModel cycle) async {
    final box = await Hive.openBox<MenstrualCycleModel>(boxName);
    // We only need to store one active cycle configuration for now
    await box.put('current_cycle', cycle);
  }

  Future<MenstrualCycleModel?> getCycle() async {
    final box = await Hive.openBox<MenstrualCycleModel>(boxName);
    return box.get('current_cycle');
  }
}
