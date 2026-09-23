import 'package:hive_flutter/hive_flutter.dart';
import '../models/reminder_model.dart';

class ReminderModelAdapter extends TypeAdapter<ReminderModel> {
  @override
  final int typeId = 0;

  @override
  ReminderModel read(BinaryReader reader) {
    return ReminderModel(
      title: reader.readString(),
      subtitle: reader.readString(),
      tagText: reader.readString(),
      tagColor: reader.read(), // Uses ColorAdapter
      icon: reader.read(), // Uses IconDataAdapter
      time: reader.readString(),
      imageUrl: reader.read(), // Nullable String
      isCompleted: reader.readBool(),
      isMissed: reader.readBool(),
      isUrgent: reader.readBool(),
    );
  }

  @override
  void write(BinaryWriter writer, ReminderModel obj) {
    writer.writeString(obj.title);
    writer.writeString(obj.subtitle);
    writer.writeString(obj.tagText);
    writer.write(obj.tagColor);
    writer.write(obj.icon);
    writer.writeString(obj.time);
    writer.write(obj.imageUrl);
    writer.writeBool(obj.isCompleted);
    writer.writeBool(obj.isMissed);
    writer.writeBool(obj.isUrgent);
  }
}
