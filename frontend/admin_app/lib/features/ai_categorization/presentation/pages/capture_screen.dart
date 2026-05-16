import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import 'ai_scan_result_screen.dart';

/// AI Document Categorization intro screen — mirrors patient_app approach.
/// Uses plain Navigator.push for AiScanResultScreen (camera-heavy screen).
class CaptureScreen extends StatelessWidget {
  const CaptureScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'AI Categorization',
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
          onPressed: () => context.pop(),
        ),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 16.h),
        child: Column(
          children: [
            SizedBox(height: 20.h),

            // Header icon
            Container(
              padding: EdgeInsets.all(20.w),
              decoration: const BoxDecoration(
                color: Color(0xFFE0F2F1),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.copy_all_rounded,
                size: 60,
                color: Color(0xFF10B981),
              ),
            ),

            SizedBox(height: 16.h),

            // Title
            const Text(
              'AI Document Categorization',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: Color(0xFF111827),
              ),
            ),

            SizedBox(height: 12.h),

            // Description
            const Text(
              'Skip the manual entry. Our secure AI analyzes your medical document to automatically detect types and extract details.',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 14,
                color: Color(0xFF6B7280),
                height: 1.5,
              ),
            ),

            SizedBox(height: 32.h),

            // Steps
            _buildStepCard(
              icon: Icons.camera_alt_outlined,
              iconColor: const Color(0xFF3B82F6),
              title: '1. Capture or Upload',
              description:
                  'Take a clear photo of your document or upload a PDF/Image',
            ),
            SizedBox(height: 16.h),
            _buildStepCard(
              icon: Icons.psychology_outlined,
              iconColor: const Color(0xFF8B5CF6),
              title: '2. Smart Analysis',
              description:
                  'AI identifies if it\'s a lab result, prescription or doctor\'s note.',
            ),
            SizedBox(height: 16.h),
            _buildStepCard(
              icon: Icons.check_circle_outline,
              iconColor: const Color(0xFF10B981),
              title: '3. Review and Save',
              description:
                  'Quickly verify the extracted data and save to your records.',
            ),

            SizedBox(height: 32.h),

            // Scan button — uses plain Navigator like patient_app
            SizedBox(
              width: double.infinity,
              height: 56.h,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          const AiScanResultScreen(autoLaunchCamera: true),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 2,
                ),
                icon: const Icon(Icons.document_scanner_outlined),
                label: const Text(
                  'Scan Document with AI',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),

            SizedBox(height: 16.h),

            // Dictate button — admin-only feature, uses GoRouter
            TextButton.icon(
              onPressed: () => context.push('/voice_dictation'),
              icon: const Icon(
                Icons.mic_none,
                size: 20,
                color: Color(0xFF374151),
              ),
              label: const Text(
                'Dictate',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w500,
                  color: Color(0xFF374151),
                ),
              ),
            ),

            SizedBox(height: 40.h),
          ],
        ),
      ),
    );
  }

  Widget _buildStepCard({
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
            color: Colors.black.withValues(alpha: 0.02),
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
              color: iconColor.withValues(alpha: 0.1),
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
