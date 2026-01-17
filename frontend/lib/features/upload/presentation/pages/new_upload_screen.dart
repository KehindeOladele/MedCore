import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../../../../features/upload/presentation/pages/upload_result_screen.dart';

class NewUploadScreen extends StatelessWidget {
  const NewUploadScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          "New Upload",
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Choose which medical\nrecord to upload",
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                height: 1.2,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              "Select a category to organize your health records efficiently.",
              style: TextStyle(fontSize: 14, color: Colors.grey[600]),
            ),
            const SizedBox(height: 32),

            // Grid
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio:
                  0.75, // Adjust aspect ratio for card height to prevent overflow
              children: [
                _buildUploadCategory(
                  context,
                  iconPath: 'assets/icons/lab_test.svg',
                  color: const Color(0xFFE0F2F1), // Light Mint
                  title: "Lab Test",
                  description: "Blood work, urine\nanalysis, pathology",
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const UploadResultScreen(),
                      ),
                    );
                  },
                ),
                _buildUploadCategory(
                  context,
                  iconPath: 'assets/icons/imaging.svg',
                  color: const Color(0xFFE3F2FD), // Light Blue
                  title: "Imaging",
                  description: "X-rays, MRI scans, CT\nscans, Ultrasounds",
                ),
                _buildUploadCategory(
                  context,
                  iconPath: 'assets/icons/prescription.svg',
                  color: const Color(0xFFE0F7FA), // Light Cyan
                  title: "Prescription",
                  description: "Medication lists, Rx\nslips, renewals",
                ),
                _buildUploadCategory(
                  context,
                  iconPath: 'assets/icons/report.svg',
                  color: const Color(0xFFF3E5F5), // Light Purple
                  title: "Report/Note",
                  description: "Doctor's notes,\ndischarge summary",
                ),
              ],
            ),

            const SizedBox(height: 32),

            // AI Suggestion Card
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
              decoration: BoxDecoration(
                color: Colors.white,
                border: Border.all(
                  color: const Color(0xFFCCFBF1),
                  width: 1.5,
                ), // Soft teal border
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: const Color(
                      0xFF10B981,
                    ).withOpacity(0.08), // Colored shadow
                    blurRadius: 20,
                    offset: const Offset(0, 8),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Container(
                    width: 56,
                    height: 56,
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981), // Emerald Green
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF10B981).withOpacity(0.3),
                          blurRadius: 12,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: const Icon(
                      Icons.auto_awesome,
                      color: Colors.white,
                      size: 28,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Don't know what record\nit is?",
                          style: TextStyle(
                            fontWeight: FontWeight.w800, // Extra bold
                            fontSize: 16,
                            height: 1.2,
                            color: Color(0xFF111827), // Gray 900
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          "Let our AI categorize your\ndocument automatically.",
                          style: TextStyle(
                            color: Color(0xFF6B7280), // Gray 500
                            fontSize: 13,
                            height: 1.4,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF9FAFB), // Gray 50
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(
                      Icons.arrow_forward,
                      size: 20,
                      color: Color(0xFF9CA3AF), // Gray 400
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUploadCategory(
    BuildContext context, {
    required String iconPath,
    required Color color,
    required String title,
    required String description,
    VoidCallback? onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey.withOpacity(0.1)),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.03),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: color, shape: BoxShape.circle),
              child: SvgPicture.asset(iconPath, width: 24, height: 24),
            ),
            const Spacer(),
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Text(
              description,
              style: TextStyle(
                color: Colors.grey[500],
                fontSize: 12,
                height: 1.4,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
