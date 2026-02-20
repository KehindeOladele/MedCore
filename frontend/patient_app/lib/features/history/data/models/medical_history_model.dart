class MedicalHistoryItem {
  final DateTime date;
  final String title;
  final String subtitle; // Doctor name or Refill #
  final String description; // Diagnosis or Drug name
  final String? actionText;
  final String type; // 'diagnosis', 'pharmacy', 'lab'

  MedicalHistoryItem({
    required this.date,
    required this.title,
    required this.subtitle,
    required this.description,
    this.actionText,
    required this.type,
  });
}
