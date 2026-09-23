import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';

class PatientRecordsScreen extends StatelessWidget {
  const PatientRecordsScreen({super.key});

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
          'Patient Records',
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 18.sp,
            fontWeight: FontWeight.w700,
            fontFamily: 'Inter',
          ),
        ),
        centerTitle: true,
        actions: [
          Padding(
            padding: EdgeInsets.only(right: 24.w),
            child: Container(
              width: 40,
              height: 40,
              decoration: const BoxDecoration(
                color: Color(0xFF059669),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Color.fromRGBO(5, 150, 105, 0.3),
                    blurRadius: 10,
                    offset: Offset(0, 4),
                  ),
                ],
              ),
              child: IconButton(
                icon: const Icon(Icons.add, color: Colors.white, size: 24),
                onPressed: () {},
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: EdgeInsets.only(left: 24.w, right: 24.w, bottom: 24.h),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: 24.h),
                  _buildPatientProfileHeader(context),
                  SizedBox(height: 24.h),
                  _buildBloodAndGenotype(),
                  SizedBox(height: 24.h),
                  _buildQuickVitals(),
                  SizedBox(height: 24.h),
                  _buildAllergiesAlerts(),
                  SizedBox(height: 24.h),
                  _buildClinicalSummary(),
                  SizedBox(height: 32.h),
                  _buildActivePrescriptions(),
                  SizedBox(height: 32.h),
                  _buildActivityTimeline(),
                ],
              ),
            ),
          ),
          // Bottom button
          Container(
            padding: EdgeInsets.fromLTRB(24.w, 16.h, 24.w, 32.h),
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
            child: SizedBox(
              width: double.infinity,
              height: 56.h,
              child: ElevatedButton(
                onPressed: () {
                  context.push('/add_clinical_note');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF059669),
                  foregroundColor: Colors.white,
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(28),
                  ),
                ),
                child: Text(
                  'Begin Diagnosis',
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
    );
  }

  Widget _buildPatientProfileHeader(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            shape: BoxShape.rectangle,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: const Color(0xFFF1F5F9), width: 3),
            image: const DecorationImage(
              image: AssetImage(
                'assets/images/doctor_avatar.png',
              ), // Replace with patient photo later
              fit: BoxFit.cover,
            ),
          ),
        ),
        SizedBox(width: 16.w),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Luke Maxwell',
                style: TextStyle(
                  color: const Color(0xFF0F172A),
                  fontSize: 20.sp,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'Inter',
                  letterSpacing: -0.5,
                ),
              ),
              SizedBox(height: 4.h),
              Text(
                '34 Yrs • Male • ID: MED-882190',
                style: TextStyle(
                  color: const Color(0xFF64748B),
                  fontSize: 13.sp,
                  fontWeight: FontWeight.w500,
                  fontFamily: 'Inter',
                ),
              ),
              SizedBox(height: 12.h),
              InkWell(
                onTap: () {
                  context.push('/patient_history');
                },
                borderRadius: BorderRadius.circular(20),
                child: Container(
                  padding: EdgeInsets.symmetric(
                    horizontal: 16.w,
                    vertical: 8.h,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFF059669),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    'View Full Medical History',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildBloodAndGenotype() {
    return Row(
      children: [
        Expanded(
          child: Container(
            padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 16.h),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFFF8FAFC), width: 2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'BLOOD GROUP',
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 10.sp,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.0,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 8.h),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.baseline,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Text(
                      'A+',
                      style: TextStyle(
                        color: const Color(0xFF0F172A),
                        fontSize: 20.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                      ),
                    ),
                    SizedBox(width: 8.w),
                    Text(
                      'Rh Positive',
                      style: TextStyle(
                        color: const Color(0xFF10B981),
                        fontSize: 10.sp,
                        fontWeight: FontWeight.w600,
                        fontFamily: 'Inter',
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
        SizedBox(width: 16.w),
        Expanded(
          child: Container(
            padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 16.h),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFFF8FAFC), width: 2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'GENOTYPE',
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 10.sp,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.0,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 8.h),
                Text(
                  'AA',
                  style: TextStyle(
                    color: const Color(0xFF0F172A),
                    fontSize: 20.sp,
                    fontWeight: FontWeight.w700,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildQuickVitals() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 20.h),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFF8FAFC), width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'QUICK VITALS',
            style: TextStyle(
              color: const Color(0xFF94A3B8),
              fontSize: 11.sp,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.5,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 20.h),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _buildVitalItem(
                'BP',
                '120/80',
                'Normal',
                const Color(0xFF10B981),
              ),
              _buildVerticalDivider(),
              _buildVitalItem(
                'Heart Rate',
                '72 bpm',
                'Steady',
                const Color(0xFF10B981),
              ),
              _buildVerticalDivider(),
              _buildVitalItem(
                'Blood sugar level',
                '98%',
                'Optimal',
                const Color(0xFF10B981),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildVitalItem(
    String title,
    String value,
    String status,
    Color statusColor,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          title,
          style: TextStyle(
            color: const Color(0xFF94A3B8),
            fontSize: 10.sp,
            fontWeight: FontWeight.w500,
            fontFamily: 'Inter',
          ),
        ),
        SizedBox(height: 6.h),
        Text(
          value,
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 16.sp,
            fontWeight: FontWeight.w700,
            fontFamily: 'Inter',
          ),
        ),
        SizedBox(height: 4.h),
        Text(
          status,
          style: TextStyle(
            color: statusColor,
            fontSize: 10.sp,
            fontWeight: FontWeight.w600,
            fontFamily: 'Inter',
          ),
        ),
      ],
    );
  }

  Widget _buildVerticalDivider() {
    return Container(height: 40, width: 1, color: const Color(0xFFF1F5F9));
  }

  Widget _buildAllergiesAlerts() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: const Color(0xFFFEF2F2),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color.fromRGBO(239, 68, 68, 0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.warning_amber_rounded,
                color: Color(0xFFEF4444),
                size: 20,
              ),
              SizedBox(width: 8.w),
              Text(
                'ALLERGIES & ALERTS',
                style: TextStyle(
                  color: const Color(0xFFEF4444),
                  fontSize: 11.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.5,
                  fontFamily: 'Inter',
                ),
              ),
            ],
          ),
          SizedBox(height: 16.h),
          Wrap(
            spacing: 8.w,
            runSpacing: 8.h,
            children: [
              _buildAllergyChip('Penicillin'),
              _buildAllergyChip('Latex'),
              _buildAllergyChip('Peanuts'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAllergyChip(String label) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 8.h),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: const Color(0xFFEF4444),
          fontSize: 12.sp,
          fontWeight: FontWeight.w600,
          fontFamily: 'Inter',
        ),
      ),
    );
  }

  Widget _buildClinicalSummary() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFF8FAFC), width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'CURRENT CLINICAL SUMMARY',
            style: TextStyle(
              color: const Color(0xFF94A3B8),
              fontSize: 11.sp,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.5,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 16.h),
          Text(
            'Patient presented with recurring acute chest pain and mild dyspnea. Initial ECG shows non-specific ST-segment changes. Monitoring for potential cardiac event.',
            style: TextStyle(
              color: const Color(0xFF475569),
              fontSize: 14.sp,
              fontWeight: FontWeight.w400,
              height: 1.6,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActivePrescriptions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'ACTIVE PRESCRIPTIONS',
              style: TextStyle(
                color: const Color(0xFF94A3B8),
                fontSize: 11.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
                fontFamily: 'Inter',
              ),
            ),
            Text(
              '4 Total',
              style: TextStyle(
                color: const Color(0xFF10B981),
                fontSize: 12.sp,
                fontWeight: FontWeight.w600,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
        SizedBox(height: 16.h),
        SizedBox(
          height: 160.h,
          child: ListView(
            scrollDirection: Axis.horizontal,
            clipBehavior: Clip.none,
            children: [
              _buildPrescriptionCard(
                title: 'Amoxicillin',
                dosage: '500mg • 2x Daily',
                iconColor: const Color(0xFF10B981),
                bgColor: const Color.fromRGBO(16, 185, 129, 0.1),
                icon: Icons.medication,
                progressColor: const Color(0xFF10B981),
                progressText: '',
              ),
              SizedBox(width: 16.w),
              _buildPrescriptionCard(
                title: 'Lisinopril',
                dosage: '10mg • 1x Daily',
                iconColor: const Color(0xFF3B82F6),
                bgColor: const Color.fromRGBO(59, 130, 246, 0.1),
                icon: Icons.water_drop,
                progressColor: const Color(0xFF3B82F6),
                progressText: '',
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildPrescriptionCard({
    required String title,
    required String dosage,
    required Color iconColor,
    required Color bgColor,
    required IconData icon,
    required Color progressColor,
    required String progressText, // e.g. "80%" width roughly
  }) {
    return Container(
      width: 180.w,
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(color: bgColor, shape: BoxShape.circle),
            child: Icon(icon, color: iconColor, size: 20),
          ),
          const Spacer(),
          Text(
            title,
            style: TextStyle(
              color: const Color(0xFF0F172A),
              fontSize: 16.sp,
              fontWeight: FontWeight.w700,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 4.h),
          Text(
            dosage,
            style: TextStyle(
              color: const Color(0xFF94A3B8),
              fontSize: 12.sp,
              fontWeight: FontWeight.w500,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 12.h),
          // Progress Bar
          Container(
            height: 4.h,
            width: double.infinity,
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(2),
            ),
            child: Row(
              children: [
                Expanded(
                  flex: 2,
                  child: Container(
                    decoration: BoxDecoration(
                      color: progressColor,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                Expanded(flex: 1, child: Container()),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActivityTimeline() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'ACTIVITY TIMELINE',
              style: TextStyle(
                color: const Color(0xFF94A3B8),
                fontSize: 11.sp,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
                fontFamily: 'Inter',
              ),
            ),
            Text(
              'View all',
              style: TextStyle(
                color: const Color(0xFF10B981),
                fontSize: 12.sp,
                fontWeight: FontWeight.w600,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
        SizedBox(height: 24.h),
        _buildTimelineItem(
          title: 'Vitals Checked',
          subtitle: 'Registered by Nurse Mark • 15 mins ago',
          isFirst: true,
          isActive: true,
        ),
        _buildTimelineItem(
          title: 'New Lab Results',
          subtitle: 'Complete Blood Count • 2 hours ago',
          isActive: true,
          actionButton: 'Download PDF',
        ),
        _buildTimelineItem(
          title: 'Medication Administered',
          subtitle: 'Amoxicillin 500mg • 4 hours ago',
          isLast: true,
          isActive: false,
        ),
      ],
    );
  }

  Widget _buildTimelineItem({
    required String title,
    required String subtitle,
    bool isFirst = false,
    bool isLast = false,
    bool isActive = true,
    String? actionButton,
  }) {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Line & Dot
          SizedBox(
            width: 24.w,
            child: Column(
              children: [
                Container(
                  height: isFirst ? 0 : 20.h,
                  width: 2,
                  color: isFirst ? Colors.transparent : const Color(0xFFE2E8F0),
                ),
                Container(
                  width: 16,
                  height: 16,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isActive
                        ? const Color(0xFF10B981)
                        : const Color(0xFFCBD5E1),
                    border: Border.all(color: Colors.white, width: 3),
                    boxShadow: [
                      if (isActive)
                        BoxShadow(
                          color: const Color(0xFF10B981).withValues(alpha: 0.3),
                          blurRadius: 4,
                          spreadRadius: 2,
                        ),
                    ],
                  ),
                ),
                Expanded(
                  child: Container(
                    width: 2,
                    color: isLast
                        ? Colors.transparent
                        : const Color(0xFFE2E8F0),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(width: 16.w),
          // Content
          Expanded(
            child: Padding(
              padding: EdgeInsets.only(bottom: 32.h, top: isFirst ? 0 : 16.h),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      color: const Color(0xFF0F172A),
                      fontSize: 14.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                    ),
                  ),
                  SizedBox(height: 4.h),
                  Text(
                    subtitle,
                    style: TextStyle(
                      color: const Color(0xFF94A3B8),
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w400,
                      fontFamily: 'Inter',
                    ),
                  ),
                  if (actionButton != null) ...[
                    SizedBox(height: 12.h),
                    InkWell(
                      onTap: () {},
                      borderRadius: BorderRadius.circular(20),
                      child: Container(
                        padding: EdgeInsets.symmetric(
                          horizontal: 16.w,
                          vertical: 6.h,
                        ),
                        decoration: BoxDecoration(
                          color: const Color.fromRGBO(5, 150, 105, 0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          actionButton,
                          style: TextStyle(
                            color: const Color(0xFF059669),
                            fontSize: 12.sp,
                            fontWeight: FontWeight.w600,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
