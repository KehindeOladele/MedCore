class ProfileModel {
  final String id;
  final String firstName;
  final String lastName;
  final String? middleName;
  final DateTime? dateOfBirth;
  final String? gender;
  final String? bloodGroup;
  final String? maritalStatus;
  final String? phone;
  final String? email;
  final String? address;
  final String? emergencyContactName;
  final String? emergencyContactPhone;
  final String? profileImageUrl;
  final Map<String, dynamic> fhirMetadata;

  ProfileModel({
    required this.id,
    required this.firstName,
    required this.lastName,
    this.middleName,
    this.dateOfBirth,
    this.gender,
    this.bloodGroup,
    this.maritalStatus,
    this.phone,
    this.email,
    this.address,
    this.emergencyContactName,
    this.emergencyContactPhone,
    this.profileImageUrl,
    this.fhirMetadata = const {},
  });

  factory ProfileModel.fromJson(Map<String, dynamic> json) {
    return ProfileModel(
      id: json['id'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      middleName: json['middle_name'],
      dateOfBirth: json['date_of_birth'] != null 
          ? DateTime.tryParse(json['date_of_birth']) 
          : null,
      gender: json['gender'],
      bloodGroup: json['blood_group'],
      maritalStatus: json['marital_status'],
      phone: json['phone'],
      email: json['email'],
      address: json['address'],
      emergencyContactName: json['emergency_contact_name'],
      emergencyContactPhone: json['emergency_contact_phone'],
      profileImageUrl: json['profile_image_url'],
      fhirMetadata: json['fhir_metadata'] ?? {},
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'first_name': firstName,
      'last_name': lastName,
      'middle_name': middleName,
      'date_of_birth': dateOfBirth?.toIso8601String().split('T').first,
      'gender': gender,
      'blood_group': bloodGroup,
      'marital_status': maritalStatus,
      'phone': phone,
      'email': email,
      'address': address,
      'emergency_contact_name': emergencyContactName,
      'emergency_contact_phone': emergencyContactPhone,
      'profile_image_url': profileImageUrl,
      'fhir_metadata': fhirMetadata,
    };
  }

  String get fullName {
    if (middleName != null && middleName!.isNotEmpty) {
      return '$firstName $middleName $lastName';
    }
    return '$firstName $lastName';
  }

  double? get height => fhirMetadata['height'] != null ? (fhirMetadata['height'] as num).toDouble() : null;
  double? get weight => fhirMetadata['weight'] != null ? (fhirMetadata['weight'] as num).toDouble() : null;
  String? get genotype => fhirMetadata['genotype'];
  List<String> get allergies {
    final list = fhirMetadata['allergies'];
    if (list is List) {
      return list.map((e) => e.toString()).toList();
    }
    return [];
  }
}
