class MedicalHistoryItem {
  final String id;
  final DateTime date;
  final String title;
  final String subtitle; // Doctor name or Refill #
  final String description; // Diagnosis or Drug name
  final String? actionText;
  final String type; // 'diagnosis', 'pharmacy', 'lab'

  MedicalHistoryItem({
    this.id = '',
    required this.date,
    required this.title,
    required this.subtitle,
    required this.description,
    this.actionText,
    required this.type,
  });

  factory MedicalHistoryItem.fromJson(Map<String, dynamic> json) {
    return MedicalHistoryItem(
      id: json['id'] ?? '',
      date: json['eventDate'] != null 
          ? DateTime.tryParse(json['eventDate']) ?? DateTime.now() 
          : DateTime.now(),
      title: json['eventType'] ?? 'Medical Record',
      subtitle: json['providerName'] ?? json['facilityName'] ?? 'Unknown Provider',
      description: json['description'] ?? '',
      type: (json['eventType'] ?? '').toString().toLowerCase().contains('lab') 
          ? 'lab' 
          : 'diagnosis',
      actionText: (json['eventType'] ?? '').toString().toLowerCase().contains('lab') 
          ? 'VIEW LAB RESULT' 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'eventDate': date.toIso8601String(),
      'eventType': title,
      'providerName': subtitle,
      'description': description,
    };
  }
}
