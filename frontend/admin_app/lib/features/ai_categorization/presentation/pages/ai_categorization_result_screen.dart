import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../../../patient_history/data/models/medical_history_model.dart';
import '../../../patient_history/data/repositories/patient_history_repository.dart';

/// SOAP Note Structure review screen shown after "Begin Categorization".
class AiCategorizationResultScreen extends StatefulWidget {
  const AiCategorizationResultScreen({super.key});

  @override
  State<AiCategorizationResultScreen> createState() =>
      _AiCategorizationResultScreenState();
}

class _AiCategorizationResultScreenState
    extends State<AiCategorizationResultScreen> {
  final TextEditingController _subjectiveCtrl = TextEditingController(
    text:
        'Lorem ipsum dolor sit amet consectetur. Tempus vestibulum at tristique uma ullamcorper senectus. Lectus consectetur diam tincidunt at aliquam elit ut pulvinar. Vitae magna euismod vestibulum dolor commodo arcu. Consequat.',
  );

  final TextEditingController _assessmentCtrl = TextEditingController(
    text:
        'Lorem ipsum dolor sit amet consectetur. Ac tristique uma ullamcorper senectus. Lectus consectetur diam tincidunt at aliquam elit ut pulvinar.',
  );

  final TextEditingController _planCtrl = TextEditingController(
    text:
        '1. Lorem ipsum dolor sit at arcu consectetur.\n2. Tempus vestibulum at tristique uma ullamcorper senectus.\n3. Lectus consectetur diam tincidunt elit ut pulvinar.',
  );

  @override
  void dispose() {
    _subjectiveCtrl.dispose();
    _assessmentCtrl.dispose();
    _planCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        scrolledUnderElevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
          onPressed: () => context.pop(),
        ),
        title: Text(
          'AI Categorization Result',
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 17.sp,
            fontWeight: FontWeight.w700,
            fontFamily: 'Inter',
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: EdgeInsets.fromLTRB(20.w, 20.h, 20.w, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ── Header ──
                  _buildHeader(),
                  SizedBox(height: 20.h),

                  // ── SUBJECTIVE ──
                  _buildSection(
                    label: 'SUBJECTIVE',
                    tag: "Patient's complaint & history",
                    controller: _subjectiveCtrl,
                    minLines: 4,
                  ),
                  SizedBox(height: 16.h),

                  // ── ASSESSMENT ──
                  _buildSection(
                    label: 'ASSESSMENT',
                    tag: 'Diagnosis & Differentials',
                    controller: _assessmentCtrl,
                    minLines: 3,
                  ),
                  SizedBox(height: 16.h),

                  // ── PLAN ──
                  _buildSection(
                    label: 'PLAN',
                    tag: 'Treatments & Follow-up',
                    controller: _planCtrl,
                    minLines: 4,
                  ),
                  SizedBox(height: 24.h),
                ],
              ),
            ),
          ),

          // ── Bottom actions ──
          _buildBottomBar(context),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 14.h),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFFE2E8F0).withValues(alpha: 0.4),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
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
              fontSize: 13.sp,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSection({
    required String label,
    required String tag,
    required TextEditingController controller,
    int minLines = 3,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFFE2E8F0).withValues(alpha: 0.4),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Section header row
          Padding(
            padding: EdgeInsets.fromLTRB(16.w, 14.h, 16.w, 0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  label,
                  style: TextStyle(
                    color: const Color(0xFF64748B),
                    fontSize: 11.sp,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.0,
                    fontFamily: 'Inter',
                  ),
                ),
                Text(
                  tag,
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 11.sp,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 10.h),

          // Toolbar
          _buildToolbar(),

          const Divider(height: 1, color: Color(0xFFF1F5F9)),
          SizedBox(height: 8.h),

          // Text field
          Padding(
            padding: EdgeInsets.fromLTRB(16.w, 0, 16.w, 14.h),
            child: TextField(
              controller: controller,
              minLines: minLines,
              maxLines: null,
              style: TextStyle(
                color: const Color(0xFF334155),
                fontSize: 13.sp,
                height: 1.6,
                fontFamily: 'Inter',
              ),
              decoration: const InputDecoration(
                border: InputBorder.none,
                isCollapsed: true,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildToolbar() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 12.w, vertical: 6.h),
      child: Row(
        children: [
          _toolbarBtn(Icons.format_bold, 'Bold'),
          _toolbarBtn(Icons.format_italic, 'Italic'),
          _toolbarBtn(Icons.format_list_bulleted, 'List'),
          _toolbarBtn(Icons.access_time_outlined, 'Timestamp'),
        ],
      ),
    );
  }

  Widget _toolbarBtn(IconData icon, String tooltip) {
    return Tooltip(
      message: tooltip,
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: () {},
        child: Padding(
          padding: EdgeInsets.all(6.w),
          child: Icon(icon, size: 18.sp, color: const Color(0xFF64748B)),
        ),
      ),
    );
  }

  Widget _buildBottomBar(BuildContext context) {
    return Container(
      padding: EdgeInsets.fromLTRB(20.w, 16.h, 20.w, 32.h),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Confirm & Save
          SizedBox(
            width: double.infinity,
            height: 52.h,
            child: ElevatedButton(
              onPressed: () {
                // ADD TO MEDICAL HISTORY
                PatientHistoryRepository.instance.addItem(
                  MedicalHistoryItem(
                    date: DateTime.now(),
                    title: "General Hospital", // From the hardcoded data
                    subtitle: "Dr. Israel",
                    description:
                        "Diagnosis: Acute Bronchitis. Prescribed antibiotics and rest for 5 days.", // Simplified summary
                    actionText: "VIEW LAB RESULTS",
                    type: "diagnosis",
                  ),
                );
                context.push('/upload_confirmation');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF059669),
                foregroundColor: Colors.white,
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              child: Text(
                'Confirm & Save Records',
                style: TextStyle(
                  fontSize: 15.sp,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'Inter',
                ),
              ),
            ),
          ),
          SizedBox(height: 12.h),

          // Recategorize
          SizedBox(
            width: double.infinity,
            height: 48.h,
            child: OutlinedButton.icon(
              onPressed: () => context.pop(),
              style: OutlinedButton.styleFrom(
                foregroundColor: const Color(0xFF475569),
                side: const BorderSide(color: Color(0xFFE2E8F0)),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                backgroundColor: Colors.white,
              ),
              icon: Icon(Icons.refresh, size: 18.sp),
              label: Text(
                'Recategorize',
                style: TextStyle(
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Inter',
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
