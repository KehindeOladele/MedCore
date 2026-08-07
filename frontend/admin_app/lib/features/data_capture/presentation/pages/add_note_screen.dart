import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

class AddNoteScreen extends StatefulWidget {
  const AddNoteScreen({super.key});

  @override
  State<AddNoteScreen> createState() => _AddNoteScreenState();
}

class _AddNoteScreenState extends State<AddNoteScreen> {
  final TextEditingController _subjectiveController = TextEditingController();
  final TextEditingController _assessmentController = TextEditingController();
  final TextEditingController _planController = TextEditingController();

  @override
  void dispose() {
    _subjectiveController.dispose();
    _assessmentController.dispose();
    _planController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Add Note'), centerTitle: true),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 20.h),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Patient: Luke Maxwell', style: AppTextStyles.heading2),
              SizedBox(height: 24.h),
              _buildSection(
                title: 'Subjective Section',
                subtitle: 'Patient\'s complaint & history',
                controller: _subjectiveController,
                hintText: 'Describe symptoms and patient reports...',
                minLines: 4,
              ),
              SizedBox(height: 24.h),
              _buildSection(
                title: 'Assessment Section',
                subtitle: '',
                controller: _assessmentController,
                hintText: 'Primary diagnosis and clinical reasoning...',
                minLines: 3,
              ),
              SizedBox(height: 24.h),
              _buildSection(
                title: 'Plan Section',
                subtitle: '',
                controller: _planController,
                hintText:
                    'Outline treatment steps, prescriptions, and next visit...',
                minLines: 3,
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: Container(
        padding: EdgeInsets.all(20.w),
        decoration: BoxDecoration(
          color: AppColors.surface,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, -5),
            ),
          ],
        ),
        child: ElevatedButton(
          onPressed: () {
            // Finish and Upload
          },
          child: const Text('Finish & Upload'),
        ),
      ),
    );
  }

  Widget _buildSection({
    required String title,
    required String subtitle,
    required TextEditingController controller,
    required String hintText,
    required int minLines,
  }) {
    return Container(
      padding: EdgeInsets.all(16.w),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: AppTextStyles.heading3),
              if (subtitle.isNotEmpty)
                Text(subtitle, style: AppTextStyles.bodySmall),
            ],
          ),
          SizedBox(height: 12.h),
          // Dictate Actions Toolbar Mockup
          Row(
            children: [
              IconButton(
                onPressed: () {},
                icon: const Icon(Icons.mic_none, color: AppColors.primary),
              ),
              Container(width: 1, height: 20, color: AppColors.border),
              IconButton(
                onPressed: () {},
                icon: const Icon(
                  Icons.edit_note_outlined,
                  color: AppColors.primary,
                ),
              ),
            ],
          ),
          SizedBox(height: 8.h),
          TextField(
            controller: controller,
            maxLines: null,
            minLines: minLines,
            decoration: InputDecoration(
              hintText: hintText,
              fillColor: AppColors.background,
            ),
          ),
        ],
      ),
    );
  }
}
