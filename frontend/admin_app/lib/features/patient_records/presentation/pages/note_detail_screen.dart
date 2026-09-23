import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';

class NoteDetailScreen extends StatelessWidget {
  const NoteDetailScreen({super.key});

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
        actions: [
          IconButton(
            icon: const Icon(Icons.more_vert, color: Color(0xFF0F172A)),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 20.h),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Note header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Note Structure',
                        style: TextStyle(
                          color: const Color(0xFF0F172A),
                          fontSize: 20.sp,
                          fontWeight: FontWeight.w800,
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
                ),
                Container(
                  padding: EdgeInsets.symmetric(
                    horizontal: 12.w,
                    vertical: 6.h,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFECFDF5),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    'SOAP Note',
                    style: TextStyle(
                      color: const Color(0xFF059669),
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w600,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ],
            ),

            SizedBox(height: 8.h),
            Row(
              children: [
                const Icon(
                  Icons.person_outline,
                  size: 14,
                  color: Color(0xFF94A3B8),
                ),
                SizedBox(width: 4.w),
                Text(
                  'Dr. Israel  •  General Hospital  •  Oct 24, 2023',
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 11.sp,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),

            SizedBox(height: 24.h),
            const Divider(color: Color(0xFFF1F5F9), thickness: 1),
            SizedBox(height: 24.h),

            // SUBJECTIVE
            _buildSOAPSection(
              label: 'SUBJECTIVE',
              subtitle: "Patient's complaint & history",
              content:
                  'Patient presents with a 3-day history of productive cough, low-grade fever (37.8°C), and mild shortness of breath. '
                  'No chest pain. History of mild asthma, managed with salbutamol PRN. '
                  'Denies any recent travel or sick contacts.',
            ),

            SizedBox(height: 24.h),

            // ASSESSMENT
            _buildSOAPSection(
              label: 'ASSESSMENT',
              subtitle: 'Diagnosis & Differentials',
              content:
                  '1. Acute Bronchitis — most likely diagnosis given clinical presentation.\n'
                  '2. Community-acquired pneumonia — less likely, no consolidation on exam.\n'
                  '3. Asthma exacerbation — possible contributing factor.',
            ),

            SizedBox(height: 24.h),

            // PLAN
            _buildSOAPSection(
              label: 'PLAN',
              subtitle: 'Treatment & Next Steps',
              content:
                  '• Prescribe Amoxicillin 500mg TDS for 5 days.\n'
                  '• Continue salbutamol inhaler PRN.\n'
                  '• Advise adequate rest and hydration.\n'
                  '• Follow-up in 1 week or sooner if symptoms worsen.\n'
                  '• Order chest X-ray if no improvement in 48 hours.',
            ),

            SizedBox(height: 32.h),

            // Action buttons
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.download_outlined, size: 18),
                    label: const Text('Download PDF'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: const Color(0xFF059669),
                      side: const BorderSide(
                        color: Color(0xFF059669),
                        width: 1.5,
                      ),
                      padding: EdgeInsets.symmetric(vertical: 14.h),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 12.w),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () {},
                    icon: const Icon(
                      Icons.edit_outlined,
                      size: 18,
                      color: Colors.white,
                    ),
                    label: const Text('Edit Note'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF059669),
                      foregroundColor: Colors.white,
                      padding: EdgeInsets.symmetric(vertical: 14.h),
                      elevation: 0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 40.h),
          ],
        ),
      ),
    );
  }

  Widget _buildSOAPSection({
    required String label,
    required String subtitle,
    required String content,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: TextStyle(
                color: const Color(0xFF059669),
                fontSize: 11.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.2,
                fontFamily: 'Inter',
              ),
            ),
            Text(
              subtitle,
              style: TextStyle(
                color: const Color(0xFF94A3B8),
                fontSize: 11.sp,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
        SizedBox(height: 12.h),
        Container(
          width: double.infinity,
          padding: EdgeInsets.all(16.w),
          decoration: BoxDecoration(
            color: const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: Text(
            content,
            style: TextStyle(
              color: const Color(0xFF334155),
              fontSize: 13.sp,
              height: 1.6,
              fontFamily: 'Inter',
            ),
          ),
        ),
      ],
    );
  }
}
