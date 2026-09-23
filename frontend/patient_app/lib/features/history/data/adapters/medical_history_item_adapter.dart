import 'package:hive_flutter/hive_flutter.dart';
import '../models/medical_history_model.dart';

class MedicalHistoryItemAdapter extends TypeAdapter<MedicalHistoryItem> {
  @override
  final int typeId = 4;

  @override
  MedicalHistoryItem read(BinaryReader reader) {
    return MedicalHistoryItem(
      id: reader.readString(),
      date: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
      title: reader.readString(),
      subtitle: reader.readString(),
      description: reader.readString(),
      actionText: reader.read(), // Nullable String
      type: reader.readString(),
    );
  }

  @override
  void write(BinaryWriter writer, MedicalHistoryItem obj) {
    writer.writeString(obj.id);
    writer.writeInt(obj.date.millisecondsSinceEpoch);
    writer.writeString(obj.title);
    writer.writeString(obj.subtitle);
    writer.writeString(obj.description);
    writer.write(obj.actionText);
    writer.writeString(obj.type);
  }
}
