import 'package:flutter/material.dart';

class LabTestDetailsScreen extends StatelessWidget {
  const LabTestDetailsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB), // Light background
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          "Lab Test Details",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 20,
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Header Info Card
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.02),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: _buildHeaderItem(
                            icon: Icons.person_outline,
                            label: "ORDERED BY",
                            value: "Dr. Kehinde",
                          ),
                        ),
                        Container(
                          width: 1,
                          height: 40,
                          color: Colors.grey[200],
                        ),
                        const SizedBox(width: 24),
                        Expanded(
                          child: _buildHeaderItem(
                            icon: Icons.business_outlined,
                            label: "FACILITY",
                            value: "Garki Central Lab",
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Results Header
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        "Results",
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF1A1C1E),
                        ),
                      ),
                      TextButton(
                        onPressed: () {},
                        child: const Text(
                          "VIEW TRENDS",
                          style: TextStyle(
                            color: Color(0xFF009688),
                            fontWeight: FontWeight.bold,
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Result Cards
                  const LabResultCard(
                    title: "Total Cholesterol",
                    value: "185",
                    unit: "mg/dL",
                    refRange: "100-199 mg/dL",
                    status: LabResultStatus.normal,
                    progress: 0.7,
                  ),
                  const LabResultCard(
                    title: "LDL Cholesterol",
                    value: "112",
                    unit: "mg/dL",
                    refRange: "< 100 mg/dL",
                    status: LabResultStatus.high,
                    progress: 0.85,
                  ),
                  const LabResultCard(
                    title: "HDL Cholesterol",
                    value: "52",
                    unit: "mg/dL",
                    refRange: "> 40 mg/dL",
                    status: LabResultStatus.normal,
                    progress: 0.5,
                  ),
                  const LabResultCard(
                    title: "Triglycerides",
                    value: "168",
                    unit: "mg/dL",
                    refRange: "< 150 mg/dL",
                    status: LabResultStatus.high,
                    progress: 0.9,
                  ),
                ],
              ),
            ),
          ),

          // Bottom Button
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(
                top: BorderSide(color: Colors.grey.withOpacity(0.1)),
              ),
            ),
            child: ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.download_rounded, color: Colors.white),
              label: const Text("Download Official Report"),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF009688),
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 56),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                elevation: 0,
                textStyle: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeaderItem({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 14, color: const Color(0xFF009688)),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                color: Colors.grey[500],
                letterSpacing: 0.5,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            color: Color(0xFF1A1C1E),
          ),
        ),
      ],
    );
  }
}

enum LabResultStatus { normal, high, low }

class LabResultCard extends StatelessWidget {
  final String title;
  final String value;
  final String unit;
  final String refRange;
  final LabResultStatus status;
  final double progress; // 0.0 to 1.0 within the visual bar

  const LabResultCard({
    super.key,
    required this.title,
    required this.value,
    required this.unit,
    required this.refRange,
    required this.status,
    required this.progress,
  });

  @override
  Widget build(BuildContext context) {
    final isNormal = status == LabResultStatus.normal;
    final statusColor = isNormal
        ? const Color(0xFF00C853)
        : const Color(0xFFFF9800);
    final statusIcon = isNormal
        ? Icons.check_circle_outline
        : Icons.warning_amber_rounded;
    final statusText = isNormal
        ? "Normal"
        : (status == LabResultStatus.high ? "High" : "Low");

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: Colors.grey.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1A1C1E),
                ),
              ),
              RichText(
                text: TextSpan(
                  children: [
                    TextSpan(
                      text: value,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1A1C1E),
                      ),
                    ),
                    TextSpan(
                      text: " $unit",
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[500],
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "Ref: $refRange",
                style: TextStyle(fontSize: 12, color: Colors.grey[500]),
              ),
              Row(
                children: [
                  Icon(statusIcon, size: 14, color: statusColor),
                  const SizedBox(width: 4),
                  Text(
                    statusText,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: statusColor,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 20),
          // Progress Bar
          LayoutBuilder(
            builder: (context, constraints) {
              final width = constraints.maxWidth;

              return Stack(
                alignment: Alignment.centerLeft,
                children: [
                  // Full Background
                  Container(
                    height: 6,
                    width: width,
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),

                  // Range Visual (simplified)
                  // For normal, maybe show a green segment in middle
                  if (status == LabResultStatus.normal)
                    Container(
                      height: 6,
                      width: width * 0.6, // 60% wide
                      margin: EdgeInsets.only(left: width * 0.2), // Centered
                      decoration: BoxDecoration(
                        color: const Color(0xFF00C853).withOpacity(0.2),
                        borderRadius: BorderRadius.circular(3),
                      ),
                    )
                  else
                    Container(
                      height: 6,
                      width: width * 0.4, // 40% wide
                      margin: EdgeInsets.only(
                        left:
                            width *
                            (status == LabResultStatus.high ? 0.6 : 0.0),
                      ),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(3),
                      ),
                    ),

                  // Marker
                  Container(
                    width: 4,
                    height: 14,
                    margin: EdgeInsets.only(
                      left: (width * progress).clamp(0, width - 4),
                    ),
                    decoration: BoxDecoration(
                      color: status == LabResultStatus.normal
                          ? Colors.black
                          : statusColor,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}
