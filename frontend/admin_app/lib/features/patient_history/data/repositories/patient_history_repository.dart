import '../models/medical_history_model.dart';

class PatientHistoryRepository {
  // Mock Medical History (In-Memory for now)
  final List<MedicalHistoryItem> _medicalHistory = [
    MedicalHistoryItem(
      date: DateTime(2023, 10, 24),
      title: "St. Mary's General",
      subtitle: "Dr. Tunde Femi",
      description:
          "Diagnosis: Acute Bronchitis. Prescribed antibiotics and rest for 5 days.",
      actionText: "VIEW LAB RESULTS",
      type: "diagnosis",
    ),
    MedicalHistoryItem(
      date: DateTime(2023, 10, 10),
      title: "Igwe Pharmacy",
      subtitle: "Refill #24930",
      description: "Amoxicillin 500mg",
      type: "pharmacy",
    ),
    MedicalHistoryItem(
      date: DateTime(2023, 8, 12),
      title: "City Orthopedics",
      subtitle: "Dr. Fatima Aba",
      description:
          "Diagnosis: Sprained Ankle (Grade 2). X-Ray negative for fracture.",
      actionText: "VIEW X-RAY",
      type: "diagnosis",
    ),
  ];

  Future<List<MedicalHistoryItem>> getMedicalHistory() async {
    // Simulate delay
    await Future.delayed(const Duration(milliseconds: 400));
    return _medicalHistory;
  }
}
