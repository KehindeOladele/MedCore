import 'package:flutter/material.dart';

import '../../data/models/medical_history_model.dart';
import 'medical_records_screen.dart';
import '../../../../features/upload/presentation/pages/new_upload_screen.dart';

class MedicalHistoryScreen extends StatelessWidget {
  const MedicalHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Mock Data
    final historyItems = [
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

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Stack(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 16, 20, 0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        "Medical History",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const NewUploadScreen(),
                            ),
                          );
                        },
                        child: Container(
                          padding: const EdgeInsets.all(8),
                          decoration: const BoxDecoration(
                            color: Color(0xFF009688),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.add, color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                ),

                // Search Bar
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: "Search conditions, doctors...",
                      prefixIcon: const Icon(Icons.search, color: Colors.grey),
                      contentPadding: const EdgeInsets.symmetric(
                        vertical: 0,
                        horizontal: 20,
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(30),
                        borderSide: BorderSide(
                          color: Colors.grey.withOpacity(0.3),
                        ),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(30),
                        borderSide: BorderSide(
                          color: Colors.grey.withOpacity(0.3),
                        ),
                      ),
                    ),
                  ),
                ),

                // Timeline List
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    itemCount: historyItems.length,
                    itemBuilder: (context, index) {
                      final item = historyItems[index];
                      // Simple grouping logic for demo: Show header if first item or month changed
                      bool showHeader =
                          index == 0 ||
                          (historyItems[index].date.month !=
                              historyItems[index - 1].date.month);

                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (showHeader)
                            Padding(
                              padding: const EdgeInsets.only(
                                bottom: 16,
                                top: 8,
                              ),
                              child: Text(
                                _getMonthYear(item.date),
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          IntrinsicHeight(
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                // Timeline Indicator
                                Column(
                                  children: [
                                    Container(
                                      width: 36,
                                      height: 36,
                                      decoration: const BoxDecoration(
                                        color: Color(0xFFE0F2F1), // Light Mint
                                        shape: BoxShape.circle,
                                      ),
                                      child: Center(
                                        child: Text(
                                          "${item.date.day}",
                                          style: const TextStyle(
                                            color: Color(0xFF00695C),
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                    ),
                                    Expanded(
                                      child: Container(
                                        width: 2,
                                        color: Colors.grey.withOpacity(0.3),
                                        margin: const EdgeInsets.symmetric(
                                          vertical: 4,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(width: 16),

                                // Card
                                Expanded(
                                  child: Padding(
                                    padding: const EdgeInsets.only(bottom: 24),
                                    child: Container(
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(16),
                                        border: Border.all(
                                          color: Colors.grey.withOpacity(0.1),
                                        ),
                                        boxShadow: [
                                          BoxShadow(
                                            color: Colors.black.withOpacity(
                                              0.03,
                                            ),
                                            blurRadius: 10,
                                            offset: const Offset(0, 4),
                                          ),
                                        ],
                                      ),
                                      padding: const EdgeInsets.all(16),
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Row(
                                            children: [
                                              Container(
                                                padding: const EdgeInsets.all(
                                                  8,
                                                ),
                                                decoration: BoxDecoration(
                                                  color: item.type == 'pharmacy'
                                                      ? const Color(0xFFE0F7FA)
                                                      : const Color(0xFFE8F5E9),
                                                  borderRadius:
                                                      BorderRadius.circular(8),
                                                ),
                                                child: Icon(
                                                  item.type == 'pharmacy'
                                                      ? Icons
                                                            .assignment_outlined
                                                      : Icons
                                                            .local_hospital_outlined,
                                                  color: item.type == 'pharmacy'
                                                      ? const Color(0xFF00BCD4)
                                                      : const Color(0xFF4CAF50),
                                                  size: 20,
                                                ),
                                              ),
                                              const SizedBox(width: 12),
                                              Column(
                                                crossAxisAlignment:
                                                    CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    item.title,
                                                    style: const TextStyle(
                                                      fontWeight:
                                                          FontWeight.bold,
                                                      fontSize: 16,
                                                    ),
                                                  ),
                                                  Text(
                                                    item.subtitle,
                                                    style: TextStyle(
                                                      color: Colors.grey[600],
                                                      fontSize: 13,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ],
                                          ),
                                          const SizedBox(height: 12),
                                          Text(
                                            item.description,
                                            style: TextStyle(
                                              color: Colors.grey[800],
                                              height: 1.4,
                                            ),
                                          ),
                                          if (item.actionText != null) ...[
                                            const SizedBox(height: 16),
                                            SizedBox(
                                              width: double.infinity,
                                              child: TextButton.icon(
                                                onPressed: () {},
                                                icon: Icon(
                                                  item.actionText!.contains(
                                                        "LAB",
                                                      )
                                                      ? Icons
                                                            .description_outlined
                                                      : Icons
                                                            .calendar_view_day_outlined,
                                                  size: 18,
                                                  color: const Color(
                                                    0xFF009688,
                                                  ),
                                                ),
                                                label: Text(
                                                  item.actionText!,
                                                  style: const TextStyle(
                                                    fontWeight: FontWeight.bold,
                                                    color: Color(0xFF009688),
                                                  ),
                                                ),
                                                style: TextButton.styleFrom(
                                                  backgroundColor: const Color(
                                                    0xFFE0F2F1,
                                                  ),
                                                  shape: RoundedRectangleBorder(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                          8,
                                                        ),
                                                  ),
                                                  padding:
                                                      const EdgeInsets.symmetric(
                                                        vertical: 12,
                                                      ),
                                                ),
                                              ),
                                            ),
                                          ],
                                        ],
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                ),

                const SizedBox(height: 80), // Space for floating button
              ],
            ),
            Positioned(
              left: 20,
              right: 20,
              bottom: 20,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const MedicalRecordsScreen(),
                    ),
                  );
                },
                icon: const Icon(Icons.assignment, color: Colors.white),
                label: const Text(
                  "View Medical Record",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF009688),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 4,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getMonthYear(DateTime date) {
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    return "${months[date.month - 1]} ${date.year}";
  }
}
