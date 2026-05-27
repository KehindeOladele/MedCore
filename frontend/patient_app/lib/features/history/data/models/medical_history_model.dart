class MedicalHistoryItem {
  final String id;
  final DateTime date;
  final String title;
  final String subtitle; // Doctor name or Refill #
  final String description; // Diagnosis or Drug name
  final String? actionText;
  final String type; // 'diagnosis', 'pharmacy', 'lab', 'vaccine'
  final String? relatedLabId; // Used to navigate to lab detail screen

  MedicalHistoryItem({
    this.id = '',
    required this.date,
    required this.title,
    required this.subtitle,
    required this.description,
    this.actionText,
    required this.type,
    this.relatedLabId,
  });

  factory MedicalHistoryItem.fromJson(Map<String, dynamic> json) {
    final rawType = (json['eventType'] ?? '').toString().toLowerCase();
    final String resolvedType;
    if (rawType.contains('lab')) {
      resolvedType = 'lab';
    } else if (rawType.contains('pharmacy')) {
      resolvedType = 'pharmacy';
    } else if (rawType.contains('vaccine')) {
      resolvedType = 'vaccine';
    } else {
      resolvedType = 'diagnosis';
    }

    return MedicalHistoryItem(
      id: json['id'] ?? '',
      date: json['eventDate'] != null
          ? DateTime.tryParse(json['eventDate']) ?? DateTime.now()
          : DateTime.now(),
      // Use facilityName as the primary card title; fallback to eventType
      title: json['facilityName'] ?? json['eventType'] ?? 'Medical Visit',
      // Use providerName as subtitle; fallback to facilityName
      subtitle: json['providerName'] ?? json['facilityName'] ?? 'Unknown',
      description: json['description'] ?? '',
      type: resolvedType,
      actionText: resolvedType == 'lab' ? 'VIEW LAB RESULT' : null,
      relatedLabId: json['relatedLabId'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'eventDate': date.toIso8601String(),
      'facilityName': title,
      'providerName': subtitle,
      'description': description,
      'eventType': type,
    };
  }
}
