import 'package:hive_flutter/hive_flutter.dart';
import '../models/prescription_model.dart';

class PrescriptionModelAdapter extends TypeAdapter<PrescriptionModel> {
  @override
  final int typeId = 1;

  @override
  PrescriptionModel read(BinaryReader reader) {
    return PrescriptionModel(
      title: reader.readString(),
      subtitle: reader.readString(),
      dosage: reader.readString(),
      schedule: reader.readString(),
      icon: reader.read(), // Uses IconDataAdapter
      iconColor: reader.read(), // Uses ColorAdapter
      iconBackgroundColor: reader.read(), // Uses ColorAdapter
      badgeColor: reader.read(), // Nullable Color?
      backgroundColor: reader.read(), // Nullable Color?
    );
  }

  @override
  void write(BinaryWriter writer, PrescriptionModel obj) {
    writer.writeString(obj.title);
    writer.writeString(obj.subtitle);
    writer.writeString(obj.dosage);
    writer.writeString(obj.schedule);
    writer.write(obj.icon);
    writer.write(obj.iconColor);
    writer.write(obj.iconBackgroundColor);
    writer.write(obj.badgeColor);
    writer.write(obj.backgroundColor);
  }
}
