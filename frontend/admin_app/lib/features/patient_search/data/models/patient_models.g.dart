// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'patient_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_Patient _$PatientFromJson(Map<String, dynamic> json) => _Patient(
  id: json['id'] as String,
  firstName: json['first_name'] as String?,
  lastName: json['last_name'] as String?,
  middleName: json['middle_name'] as String?,
  dateOfBirth: json['date_of_birth'] as String?,
  gender: json['gender'] as String?,
  bloodGroup: json['blood_group'] as String?,
  maritalStatus: json['marital_status'] as String?,
  phone: json['phone'] as String?,
  email: json['email'] as String?,
  address: json['address'] as String?,
  emergencyContactName: json['emergency_contact_name'] as String?,
  emergencyContactPhone: json['emergency_contact_phone'] as String?,
  profileImageUrl: json['profile_image_url'] as String?,
  fhirMetadata: json['fhir_metadata'] as Map<String, dynamic>?,
);

Map<String, dynamic> _$PatientToJson(_Patient instance) => <String, dynamic>{
  'id': instance.id,
  'first_name': instance.firstName,
  'last_name': instance.lastName,
  'middle_name': instance.middleName,
  'date_of_birth': instance.dateOfBirth,
  'gender': instance.gender,
  'blood_group': instance.bloodGroup,
  'marital_status': instance.maritalStatus,
  'phone': instance.phone,
  'email': instance.email,
  'address': instance.address,
  'emergency_contact_name': instance.emergencyContactName,
  'emergency_contact_phone': instance.emergencyContactPhone,
  'profile_image_url': instance.profileImageUrl,
  'fhir_metadata': instance.fhirMetadata,
};
