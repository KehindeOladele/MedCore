/// Maps the backend's `GET /api/v1/user/summary` response.
class UserSummaryModel {
  final String fullName;
  final String? avatarUrl;
  final VitalsSummaryModel vitals;
  final List<ActivePrescriptionModel> activePrescriptions;
  final List<UpcomingReminderModel> upcomingReminders;

  const UserSummaryModel({
    required this.fullName,
    this.avatarUrl,
    required this.vitals,
    required this.activePrescriptions,
    required this.upcomingReminders,
  });

  factory UserSummaryModel.fromJson(Map<String, dynamic> json) {
    final user = json['user'] as Map<String, dynamic>? ?? {};
    final vitalsJson = json['vitals'] as Map<String, dynamic>? ?? {};
    final prescriptionsJson =
        (json['activePrescriptions'] as List<dynamic>?) ?? [];
    final remindersJson = (json['upcomingReminders'] as List<dynamic>?) ?? [];

    return UserSummaryModel(
      fullName: user['fullName'] as String? ?? 'Patient',
      avatarUrl: user['avatarUrl'] as String?,
      vitals: VitalsSummaryModel.fromJson(vitalsJson),
      activePrescriptions: prescriptionsJson
          .map((e) =>
              ActivePrescriptionModel.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList(),
      upcomingReminders: remindersJson
          .map((e) =>
              UpcomingReminderModel.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList(),
    );
  }
}

class VitalsSummaryModel {
  final String? bloodGroup;
  final String? genotype;
  final List<String> allergies;

  const VitalsSummaryModel({
    this.bloodGroup,
    this.genotype,
    this.allergies = const [],
  });

  factory VitalsSummaryModel.fromJson(Map<String, dynamic> json) {
    final rawAllergies = json['allergies'];
    final List<String> allergies;

    if (rawAllergies is List) {
      allergies = rawAllergies.map((e) => e.toString()).toList();
    } else {
      allergies = [];
    }

    return VitalsSummaryModel(
      bloodGroup: json['bloodGroup'] as String?,
      genotype: json['genotype'] as String?,
      allergies: allergies,
    );
  }
}

class ActivePrescriptionModel {
  final String id;
  final String drugName;
  final String? category;
  final String? dosage;
  final String? schedule;
  final String status;

  const ActivePrescriptionModel({
    required this.id,
    required this.drugName,
    this.category,
    this.dosage,
    this.schedule,
    this.status = 'active',
  });

  factory ActivePrescriptionModel.fromJson(Map<String, dynamic> json) {
    return ActivePrescriptionModel(
      id: json['id']?.toString() ?? '',
      drugName: json['drugName'] as String? ?? json['drug_name'] as String? ?? 'Unknown',
      category: json['category'] as String?,
      dosage: json['dosage'] as String?,
      schedule: json['schedule'] as String?,
      status: json['status'] as String? ?? 'active',
    );
  }
}

class UpcomingReminderModel {
  final String id;
  final String title;
  final String? subtitle;
  final String? date;
  final String type; // 'appointment' | 'medication' | 'lab'

  const UpcomingReminderModel({
    required this.id,
    required this.title,
    this.subtitle,
    this.date,
    this.type = 'appointment',
  });

  factory UpcomingReminderModel.fromJson(Map<String, dynamic> json) {
    return UpcomingReminderModel(
      id: json['id']?.toString() ?? '',
      title: json['title'] as String? ?? 'Reminder',
      subtitle: json['subtitle'] as String?,
      date: json['date'] as String? ?? json['scheduled_at'] as String?,
      type: json['type'] as String? ?? 'appointment',
    );
  }
}
