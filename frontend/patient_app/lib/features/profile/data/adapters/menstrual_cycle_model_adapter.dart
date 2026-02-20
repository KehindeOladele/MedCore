import 'package:hive_flutter/hive_flutter.dart';
import '../models/menstrual_cycle_model.dart';

class MenstrualCycleModelAdapter extends TypeAdapter<MenstrualCycleModel> {
  @override
  final int typeId = 2; // Unique ID for this type

  @override
  MenstrualCycleModel read(BinaryReader reader) {
    return MenstrualCycleModel(
      lastPeriodDate: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
      periodLength: reader.readInt(),
      cycleLength: reader.readInt(),
      flowIntensity: reader.readString(),
    );
  }

  @override
  void write(BinaryWriter writer, MenstrualCycleModel obj) {
    writer.writeInt(obj.lastPeriodDate.millisecondsSinceEpoch);
    writer.writeInt(obj.periodLength);
    writer.writeInt(obj.cycleLength);
    writer.writeString(obj.flowIntensity);
  }
}
