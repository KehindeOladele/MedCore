import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

class AiCategorizationScreen extends StatelessWidget {
  const AiCategorizationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('AI Categorization Results'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 20.h),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 16.h),
              Text('Lab Test Result', style: AppTextStyles.heading1),
              SizedBox(height: 16.h),
              Text(
                'Skip the manual entry. Our secure AI analyzes your medical document to automatically detect types and extract details.',
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              SizedBox(height: 32.h),
              _buildFeatureCard(
                title: 'Data Extraction',
                subtitle:
                    'Take a clear photo of your document or upload a PDF/Image',
                icon: Icons.camera_alt_outlined,
              ),
              SizedBox(height: 16.h),
              _buildFeatureCard(
                title: 'Smart Categorization',
                subtitle:
                    'AI identifies if its a lab result, prescription or doctor’s note.',
                icon: Icons.auto_awesome_mosaic_outlined,
              ),
              SizedBox(height: 16.h),
              _buildFeatureCard(
                title: 'Instant Verification',
                subtitle:
                    'Quickly verify the extracted data and save to your records.',
                icon: Icons.check_circle_outline,
              ),
              SizedBox(height: 48.h),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    // Navigate to document scanner
                  },
                  icon: const Icon(Icons.document_scanner),
                  label: const Text('Scan Document with AI'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.surface,
                    foregroundColor: AppColors.primary,
                    side: const BorderSide(color: AppColors.primary),
                  ),
                ),
              ),
              SizedBox(height: 16.h),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    // Navigate to Dictation
                    context.push('/dictation');
                  },
                  icon: const Icon(Icons.mic),
                  label: const Text('Dictate'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFeatureCard({
    required String title,
    required String subtitle,
    required IconData icon,
  }) {
    return Container(
      padding: EdgeInsets.all(16.w),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: EdgeInsets.all(12.w),
            decoration: BoxDecoration(
              color: AppColors.primary.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: AppColors.primary, size: 24.w),
          ),
          SizedBox(width: 16.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTextStyles.heading3),
                SizedBox(height: 4.h),
                Text(
                  subtitle,
                  style: AppTextStyles.bodyMedium.copyWith(
                    color: AppColors.textSecondary,
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
