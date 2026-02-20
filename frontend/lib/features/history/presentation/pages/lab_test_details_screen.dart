import 'package:flutter/material.dart';

class LabTestDetailsScreen extends StatelessWidget {
  const LabTestDetailsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB), // Light Gray background
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          "Lab Test Details",
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        centerTitle: false,
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
                      border: Border.all(color: Colors.grey.withOpacity(0.1)),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.02),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              "Lipid Panel",
                              style: TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.bold,
                                color: Colors.black,
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 10,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: const Color(0xFFE8F5E9),
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: const Text(
                                "● FINALIZED",
                                style: TextStyle(
                                  color: Color(0xFF2E7D32),
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "Oct 24, 2023 • 10:30 AM",
                          style: TextStyle(
                            color: Colors.grey[500],
                            fontSize: 13,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        const SizedBox(height: 24),
                        Row(
                          children: [
                            Expanded(
                              child: _buildMetadataItem(
                                icon: Icons.person_outline,
                                label: "ORDERED BY",
                                value: "Dr. Kehinde",
                              ),
                            ),
                            Expanded(
                              child: _buildMetadataItem(
                                icon: Icons
                                    .business_outlined, // Using business for facility
                                label: "FACILITY",
                                value: "Garki Central Lab",
                              ),
                            ),
                          ],
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
                          color: Colors.black,
                        ),
                      ),
                      TextButton(
                        onPressed: () {},
                        child: const Text(
                          "VIEW TRENDS",
                          style: TextStyle(
                            color: Color(0xFF00C853),
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // Result Cards
                  _buildResultCard(
                    title: "Total Cholesterol",
                    value: "185",
                    unit: "mg/dL",
                    range: "100-199 mg/dL",
                    status: "Normal",
                    statusColor: const Color(0xFF00C853),
                    normalizedValue: 0.7, // Visual position on slider
                  ),
                  const SizedBox(height: 16),
                  _buildResultCard(
                    title: "LDL Cholesterol",
                    value: "112",
                    unit: "mg/dL",
                    range: "< 100 mg/dL",
                    status: "High",
                    statusColor: const Color(0xFFFF9800), // Orange
                    normalizedValue: 0.85,
                  ),
                  const SizedBox(height: 16),
                  _buildResultCard(
                    title: "HDL Cholesterol",
                    value: "52",
                    unit: "mg/dL",
                    range: "> 40 mg/dL",
                    status: "Normal",
                    statusColor: const Color(0xFF00C853),
                    normalizedValue: 0.6,
                  ),
                  const SizedBox(height: 16),
                  _buildResultCard(
                    title: "Triglycerides",
                    value: "168",
                    unit: "mg/dL",
                    range: "< 150 mg/dL",
                    status: "High",
                    statusColor: const Color(0xFFEF5350), // Red
                    normalizedValue: 0.9,
                  ),

                  const SizedBox(height: 24),

                  // Attachments
                  const Text(
                    "Attachments",
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 16),

                  Row(
                    children: [
                      Expanded(
                        child: _buildPdfThumbnail("Full_Report.pdf", "2.4 MB"),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildPdfThumbnail(
                          "Discharge_Note.pdf",
                          "1.2 MB",
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(
                    height: 40,
                  ), // Bottom padding for scroll content
                ],
              ),
            ),
          ),
          // Fixed Bottom Button
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(
                top: BorderSide(color: Colors.grey.withOpacity(0.1)),
              ),
            ),
            child: SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF009688), // Teal color
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(25),
                  ),
                  elevation: 0,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.download, color: Colors.white, size: 20),
                    const SizedBox(width: 8),
                    const Text(
                      "Download Official Report",
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetadataItem({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 14, color: const Color(0xFF00C853)),
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
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: Colors.black87,
          ),
        ),
      ],
    );
  }

  Widget _buildResultCard({
    required String title,
    required String value,
    required String unit,
    required String range,
    required String status,
    required Color statusColor,
    required double normalizedValue,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.withOpacity(0.1)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.01),
            blurRadius: 5,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    "Ref: $range",
                    style: TextStyle(fontSize: 12, color: Colors.grey[500]),
                  ),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        value,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.black,
                        ),
                      ),
                      Text(
                        unit,
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey[500],
                          height: 1.8,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      // Status Icon (Check or Warning)
                      Icon(
                        status == "Normal"
                            ? Icons.check_circle_outline
                            : Icons.warning_amber_rounded,
                        size: 14,
                        color: statusColor,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        status,
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
            ],
          ),
          const SizedBox(height: 16),
          // Custom Slider Visualization
          Stack(
            children: [
              // Background Bar
              Container(
                height: 8, // Thicker bar
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
              // Range Bar (Visualizing the "Normal" zone approx)
              // This is a simplified visual representation
              FractionallySizedBox(
                widthFactor: 0.6, // Assume normal range covers middle 60%
                alignment: Alignment.center, // Centered
                child: Container(
                  height: 8,
                  decoration: BoxDecoration(
                    color: const Color(
                      0xFFC8E6C9,
                    ).withOpacity(0.5), // Very light green
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
              // Marker
              LayoutBuilder(
                builder: (context, constraints) {
                  // Calculate position based on normalized value (0.0 to 1.0)
                  double position = constraints.maxWidth * normalizedValue;
                  // Clamp position
                  if (position < 0) position = 0;
                  if (position > constraints.maxWidth - 4)
                    position = constraints.maxWidth - 4;

                  return Container(
                    margin: EdgeInsets.only(left: position),
                    width: 4,
                    height: 16, // Tall marker
                    transform: Matrix4.translationValues(
                      0,
                      -4,
                      0,
                    ), // Shift up to center vertically
                    decoration: BoxDecoration(
                      color: status == "Normal" ? Colors.black : statusColor,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  );
                },
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPdfThumbnail(String fileName, String size) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          height: 140,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFFFAFAFA),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.grey.withOpacity(0.1)),
          ),
          child: Center(
            child: Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                border: Border.all(color: const Color(0xFFEF5350), width: 1.5),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Center(
                child: Text(
                  "PDF",
                  style: TextStyle(
                    color: Color(0xFFEF5350),
                    fontWeight: FontWeight.bold,
                    fontSize: 10,
                  ),
                ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          fileName,
          style: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: Colors.black87,
          ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        Text(size, style: TextStyle(fontSize: 12, color: Colors.grey[500])),
      ],
    );
  }
}
