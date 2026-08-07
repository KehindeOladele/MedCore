import 'package:hive_flutter/hive_flutter.dart';
import '../models/allergy_model.dart';

class AllergyModelAdapter extends TypeAdapter<AllergyModel> {
  @override
  final int typeId = 3;

  @override
  AllergyModel read(BinaryReader reader) {
    return AllergyModel(
      id: reader.readString(),
      name: reader.readString(),
      symptoms: reader.readString(),
      severity: AllergySeverity.values[reader.readInt()],
      isCritical: reader.readBool(),
      icon: reader.read(), // Uses IconDataAdapter
      assetPath: reader.read(), // Nullable String
    );
  }

  @override
  void write(BinaryWriter writer, AllergyModel obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeString(obj.symptoms);
    writer.writeInt(obj.severity.index);
    writer.writeBool(obj.isCritical);
    writer.write(obj.icon);
    writer.write(obj.assetPath);
  }
}
