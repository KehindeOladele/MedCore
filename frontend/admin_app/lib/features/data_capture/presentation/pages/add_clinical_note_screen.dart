import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';

class AddClinicalNoteScreen extends StatefulWidget {
  const AddClinicalNoteScreen({super.key});

  @override
  State<AddClinicalNoteScreen> createState() => _AddClinicalNoteScreenState();
}

class _AddClinicalNoteScreenState extends State<AddClinicalNoteScreen> {
  final _subjectiveController = TextEditingController();
  final _assessmentController = TextEditingController();
  final _planController = TextEditingController();

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
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        scrolledUnderElevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
          onPressed: () => context.pop(),
        ),
        title: Text(
          'Clinical Notes',
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 18.sp,
            fontWeight: FontWeight.w700,
            fontFamily: 'Inter',
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 16.h),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Header Section
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Note Structure',
                              style: TextStyle(
                                color: const Color(0xFF0F172A),
                                fontSize: 18.sp,
                                fontWeight: FontWeight.w700,
                                fontFamily: 'Inter',
                              ),
                            ),
                            SizedBox(height: 4.h),
                            Text(
                              'Patient: Luke Maxwell',
                              style: TextStyle(
                                color: const Color(0xFF64748B),
                                fontSize: 12.sp,
                                fontWeight: FontWeight.w500,
                                fontFamily: 'Inter',
                              ),
                            ),
                          ],
                        ),
                        ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF059669),
                            foregroundColor: Colors.white,
                            elevation: 0,
                            padding: EdgeInsets.symmetric(
                              horizontal: 20.w,
                              vertical: 8.h,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          child: Text(
                            'Use AI',
                            style: TextStyle(
                              fontSize: 12.sp,
                              fontWeight: FontWeight.w600,
                              fontFamily: 'Inter',
                            ),
                          ),
                        ),
                      ],
                    ),

                    SizedBox(height: 32.h),

                    // Subjective Section
                    _buildNoteSection(
                      title: 'SUBJECTIVE',
                      subtitle: "Patient's complaint & history",
                      hintText: 'Describe symptoms and patient reports...',
                      controller: _subjectiveController,
                    ),

                    SizedBox(height: 24.h),

                    // Assessment Section
                    _buildNoteSection(
                      title: 'ASSESSMENT',
                      subtitle: "Diagnosis & Differentials",
                      hintText: 'Primary diagnosis and clinical reasoning...',
                      controller: _assessmentController,
                    ),

                    SizedBox(height: 24.h),

                    // Plan Section
                    _buildNoteSection(
                      title: 'PLAN',
                      subtitle: "Treatments & Follow-up",
                      hintText:
                          'Outline treatment steps, prescriptions, and next visit...',
                      controller: _planController,
                    ),

                    SizedBox(height: 32.h),

                    // Bottom Tool Buttons
                    Row(
                      children: [
                        _buildToolButton(
                          icon: Icons.mic_none,
                          label: 'Dictate',
                          color: const Color(0xFF059669),
                          onTap: () {},
                        ),
                        SizedBox(width: 12.w),
                        _buildToolButton(
                          icon: Icons
                              .filter_center_focus, // Scan/Photo icon substitute
                          label: 'Take Photo',
                          color: const Color(0xFF64748B),
                          onTap: () {},
                        ),
                        SizedBox(width: 12.w),
                        InkWell(
                          onTap: () {},
                          borderRadius: BorderRadius.circular(20),
                          child: Container(
                            padding: EdgeInsets.all(10.w),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              border: Border.all(
                                color: const Color(0xFFE2E8F0),
                              ),
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              Icons.attach_file,
                              color: const Color(0xFF64748B),
                              size: 18.sp,
                            ),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 48.h),
                  ],
                ),
              ),
            ),

            // Finish & Upload Button
            Padding(
              padding: EdgeInsets.only(
                left: 24.w,
                right: 24.w,
                bottom: 24.h,
                top: 16.h,
              ),
              child: SizedBox(
                width: double.infinity,
                height: 56.h,
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF059669),
                    foregroundColor: Colors.white,
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(28),
                    ),
                  ),
                  child: Text(
                    'Finish & Upload',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNoteSection({
    required String title,
    required String subtitle,
    required String hintText,
    required TextEditingController controller,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: TextStyle(
                color: const Color(0xFF64748B),
                fontSize: 11.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.0,
                fontFamily: 'Inter',
              ),
            ),
            Text(
              subtitle,
              style: TextStyle(
                color: const Color(0xFF94A3B8),
                fontSize: 10.sp,
                fontWeight: FontWeight.w500,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
        SizedBox(height: 8.h),
        // Use a Focus widget to detect focus changes and color the border dynamically
        Focus(
          child: Builder(
            builder: (context) {
              final isFocused = Focus.of(context).hasFocus;
              return AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isFocused
                        ? const Color(0xFF059669)
                        : const Color(0xFFE2E8F0),
                    width: isFocused ? 1.5 : 1.0,
                  ),
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(
                    11,
                  ), // Slightly less to fit inside border
                  child: Column(
                    children: [
                      // Toolbar
                      Container(
                        padding: EdgeInsets.symmetric(
                          horizontal: 12.w,
                          vertical: 8.h,
                        ),
                        decoration: const BoxDecoration(
                          border: Border(
                            bottom: BorderSide(color: Color(0xFFF1F5F9)),
                          ),
                        ),
                        child: Row(
                          children: [
                            _buildToolbarIcon(Icons.format_bold),
                            _buildToolbarIcon(Icons.format_italic),
                            _buildToolbarIcon(Icons.format_list_bulleted),
                            if (title == 'SUBJECTIVE') ...[
                              Container(
                                width: 1,
                                height: 16.h,
                                color: const Color(0xFFE2E8F0),
                                margin: EdgeInsets.symmetric(horizontal: 8.w),
                              ),
                              _buildToolbarIcon(Icons.history),
                            ],
                          ],
                        ),
                      ),
                      // Text Field
                      TextField(
                        controller: controller,
                        maxLines: 4,
                        cursorColor: const Color(
                          0xFF059669,
                        ), // Changed generic blue cursor to brand green
                        style: TextStyle(
                          color: const Color(0xFF0F172A),
                          fontSize: 14.sp,
                          height: 1.6,
                          fontFamily: 'Inter',
                        ),
                        decoration: InputDecoration(
                          hintText: hintText,
                          hintStyle: TextStyle(
                            color: const Color(
                              0xFF94A3B8,
                            ).withValues(alpha: 0.5),
                            fontSize: 14.sp,
                            height: 1.6,
                          ),
                          border: InputBorder.none,
                          enabledBorder: InputBorder.none,
                          focusedBorder: InputBorder.none,
                          contentPadding: EdgeInsets.all(16.w),
                        ),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildToolbarIcon(IconData icon) {
    return Padding(
      padding: EdgeInsets.only(right: 12.w),
      child: Icon(icon, size: 16.sp, color: const Color(0xFF0F172A)),
    );
  }

  Widget _buildToolButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 8.h),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: const Color(0xFFE2E8F0)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 16.sp),
            SizedBox(width: 6.w),
            Text(
              label,
              style: TextStyle(
                color: const Color(0xFF0F172A),
                fontSize: 12.sp,
                fontWeight: FontWeight.w600,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
