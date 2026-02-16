import 'package:flutter/material.dart';

class AiCategorizationScreen extends StatelessWidget {
  const AiCategorizationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          "AI Categorization",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        child: Column(
          children: [
            const SizedBox(height: 20),
            // Header Icon
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: const Color(0xFFE0F2F1), // Very light teal
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.description_outlined,
                size: 80,
                color: Color(0xFF10B981), // Emerald Green
              ),
            ),
            const SizedBox(height: 24),
            // Title
            const Text(
              "AI Document Categorization",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Color(0xFF111827), // Gray 900
              ),
            ),
            const SizedBox(height: 12),
            // Description
            const Text(
              "Skip the manual entry. Our secure AI analyzes your medical document to automatically detect types and extract details.",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 14,
                color: Color(0xFF6B7280), // Gray 500
                height: 1.5,
              ),
            ),
            const SizedBox(height: 48),

            // Steps
            _buildStepCard(
              context,
              icon: Icons.camera_alt_outlined,
              iconColor: const Color(0xFF3B82F6), // Blue
              title: "1. Capture or Upload",
              description:
                  "Take a clear photo of your document or upload a PDF/Image",
            ),
            const SizedBox(height: 16),
            _buildStepCard(
              context,
              icon: Icons.psychology_outlined,
              iconColor: const Color(0xFF8B5CF6), // Purple
              title: "2. Smart Analysis",
              description:
                  "AI identifies if its a lab result, prescription or doctor's note.",
            ),
            const SizedBox(height: 16),
            _buildStepCard(
              context,
              icon: Icons.check_circle_outline,
              iconColor: const Color(0xFF10B981), // Green
              title: "3. Review and Save",
              description:
                  "Quickly verify the extracted data and save to your records.",
            ),
            const SizedBox(height: 48),

            // Buttons
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: () {
                  // TODO: Implement scan logic
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981), // Emerald Green
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 2,
                ),
                icon: const Icon(Icons.crop_free),
                label: const Text(
                  "Scan Document with AI",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 56,
              child: OutlinedButton.icon(
                onPressed: () {
                  // TODO: Implement upload from device logic
                },
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.black,
                  side: const BorderSide(color: Color(0xFFE5E7EB)),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  backgroundColor: Colors.white,
                ),
                icon: const Icon(Icons.upload_file),
                label: const Text(
                  "Upload from Device",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStepCard(
    BuildContext context, {
    required IconData icon,
    required Color iconColor,
    required String title,
    required String description,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFF3F4F6), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: iconColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: iconColor, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: Color(0xFF111827),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  description,
                  style: const TextStyle(
                    fontSize: 13,
                    color: Color(0xFF6B7280),
                    height: 1.4,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
