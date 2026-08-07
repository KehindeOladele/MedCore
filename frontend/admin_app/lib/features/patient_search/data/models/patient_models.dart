import 'package:freezed_annotation/freezed_annotation.dart';

part 'patient_models.freezed.dart';
part 'patient_models.g.dart';

@freezed
abstract class Patient with _$Patient {
  const Patient._();

  // ignore: invalid_annotation_target
  @JsonSerializable(fieldRename: FieldRename.snake)
  const factory Patient({
    required String id,
    String? firstName,
    String? lastName,
    String? middleName,
    String? dateOfBirth,
    String? gender,
    String? bloodGroup,
    String? maritalStatus,
    String? phone,
    String? email,
    String? address,
    String? emergencyContactName,
    String? emergencyContactPhone,
    String? profileImageUrl,
    Map<String, dynamic>? fhirMetadata,
  }) = _Patient;

  factory Patient.fromJson(Map<String, dynamic> json) => _$PatientFromJson(json);

  String get fullName {
    final parts = [firstName, middleName, lastName]
        .where((e) => e != null && e.isNotEmpty)
        .toList();
    if (parts.isEmpty) return 'Unknown Patient';
    return parts.join(' ');
  }

  String get age {
    if (dateOfBirth == null) return 'N/A';
    try {
      final dob = DateTime.parse(dateOfBirth!);
      final now = DateTime.now();
      int a = now.year - dob.year;
      if (now.month < dob.month ||
          (now.month == dob.month && now.day < dob.day)) {
        a--;
      }
      return '$a yrs';
    } catch (_) {
      return 'N/A';
    }
  }
}
