import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import 'note_detail_screen.dart';

class ClinicalNotesScreen extends StatelessWidget {
  const ClinicalNotesScreen({super.key});

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
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Medical Records',
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
            icon: const Icon(Icons.search, color: Color(0xFF0F172A)),
            onPressed: () {},
          ),
          SizedBox(width: 8.w),
        ],
      ),
      body: Column(
        children: [
          // ── Tab bar — Notes tab active ──────────────────────────────
          _buildTabHeader(context),
          Expanded(
            child: SingleChildScrollView(
              padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 24.h),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ── RECENT NOTES ─────────────────────────────────────
                  _buildSectionLabel('RECENT NOTES'),
                  SizedBox(height: 16.h),
                  _buildNoteCard(
                    context: context,
                    title: 'Acute Bronchitis Note',
                    doctor: 'Dr. Israel',
                    hospital: 'General Hospital',
                    date: 'Today',
                    isRecent: true,
                  ),

                  SizedBox(height: 32.h),

                  // ── PAST RECORDS ──────────────────────────────────────
                  _buildSectionLabel('PAST RECORDS'),
                  SizedBox(height: 16.h),
                  _buildNoteCard(
                    context: context,
                    title: 'Sprained Ankle Follow-up',
                    doctor: 'Dr. Fatima Aba',
                    hospital: 'City Orthopedics',
                    date: 'Aug 01',
                    isRecent: false,
                  ),
                  SizedBox(height: 16.h),
                  _buildNoteCard(
                    context: context,
                    title: 'Cardiology Referral Note',
                    doctor: 'Dr. Kehinde',
                    hospital: 'Zuma Hospital',
                    date: 'July 11',
                    isRecent: false,
                  ),
                  SizedBox(height: 16.h),
                  _buildNoteCard(
                    context: context,
                    title: 'Hypertension Review',
                    doctor: 'Dr. Kehinde',
                    hospital: 'Zuma Hospital',
                    date: 'June 02',
                    isRecent: false,
                  ),
                  SizedBox(height: 100.h),
                ],
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: _buildBottomNav(context),
    );
  }

  // ─── SECTION LABEL ────────────────────────────────────────────────
  Widget _buildSectionLabel(String label) {
    return Text(
      label,
      style: TextStyle(
        color: const Color(0xFF64748B),
        fontSize: 12.sp,
        fontWeight: FontWeight.w700,
        letterSpacing: 1.2,
        fontFamily: 'Inter',
      ),
    );
  }

  // ─── TAB HEADER ───────────────────────────────────────────────────
  Widget _buildTabHeader(BuildContext context) {
    final tabs = ['Lab Tests', 'Imaging', 'Notes', 'Prescriptions'];
    return Container(
      height: 48.h,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(
          bottom: BorderSide(color: Color(0xFFF1F5F9), width: 1.0),
        ),
      ),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.symmetric(horizontal: 16.w),
        itemCount: tabs.length,
        itemBuilder: (context, index) {
          final isSelected = index == 2; // Notes is active
          return GestureDetector(
            onTap: () {
              if (index == 0) Navigator.pop(context);
              if (index == 3) context.push('/prescriptions');
            },
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 16.w, vertical: 8.h),
              margin: EdgeInsets.only(right: 8.w, top: 4.h, bottom: 8.h),
              decoration: BoxDecoration(
                color: isSelected ? const Color(0xFF059669) : Colors.white,
                borderRadius: BorderRadius.circular(20),
                border: isSelected
                    ? null
                    : Border.all(color: const Color(0xFFF1F5F9)),
              ),
              child: Center(
                child: Text(
                  tabs[index],
                  style: TextStyle(
                    color: isSelected ? Colors.white : const Color(0xFF0F172A),
                    fontSize: 12.sp,
                    fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
                    fontFamily: 'Inter',
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  // ─── NOTE CARD ────────────────────────────────────────────────────
  Widget _buildNoteCard({
    required BuildContext context,
    required String title,
    required String doctor,
    required String hospital,
    required String date,
    required bool isRecent,
  }) {
    return Container(
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Icon
          Container(
            width: 48.w,
            height: 48.w,
            decoration: const BoxDecoration(
              color: Color(0xFFECFDF5),
              shape: BoxShape.circle,
            ),
            child: const Center(
              child: Icon(
                Icons.medical_services_outlined,
                color: Color(0xFF059669),
                size: 22,
              ),
            ),
          ),
          SizedBox(width: 16.w),

          // Info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Title row
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        title,
                        style: TextStyle(
                          color: const Color(0xFF0F172A),
                          fontSize: 15.sp,
                          fontWeight: FontWeight.w700,
                          fontFamily: 'Inter',
                        ),
                      ),
                    ),
                    if (!isRecent)
                      Text(
                        date,
                        style: TextStyle(
                          color: const Color(0xFF94A3B8),
                          fontSize: 12.sp,
                          fontFamily: 'Inter',
                        ),
                      ),
                  ],
                ),
                SizedBox(height: 4.h),

                // Doctor & hospital
                Text(
                  isRecent
                      ? '$doctor, $hospital • $date'
                      : '$doctor, $hospital',
                  style: TextStyle(
                    color: const Color(0xFF64748B),
                    fontSize: 12.sp,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 16.h),

                // PDF chip + View Note button
                Row(
                  children: [
                    // PDF chip
                    Container(
                      padding: EdgeInsets.symmetric(
                        horizontal: 10.w,
                        vertical: 5.h,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF1F5F9),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.picture_as_pdf_outlined,
                            size: 14,
                            color: Color(0xFF64748B),
                          ),
                          SizedBox(width: 4.w),
                          Text(
                            'PDF',
                            style: TextStyle(
                              color: const Color(0xFF64748B),
                              fontSize: 11.sp,
                              fontWeight: FontWeight.w600,
                              fontFamily: 'Inter',
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Spacer(),
                    // View Note → NoteDetailScreen
                    OutlinedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const NoteDetailScreen(),
                          ),
                        );
                      },
                      style: OutlinedButton.styleFrom(
                        padding: EdgeInsets.symmetric(
                          horizontal: 16.w,
                          vertical: 8.h,
                        ),
                        foregroundColor: const Color(0xFF059669),
                        side: const BorderSide(
                          color: Color(0xFF059669),
                          width: 1.5,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      child: Text(
                        'View Note',
                        style: TextStyle(
                          fontSize: 13.sp,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Inter',
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ─── BOTTOM NAV ───────────────────────────────────────────────────
  Widget _buildBottomNav(BuildContext context) {
    return Container(
      height: 68,
      decoration: BoxDecoration(
        color: Colors.white,
        border: const Border(
          top: BorderSide(color: Color(0xFFE5E7EB), width: 1),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildNavItem(
            icon: Icons.home_outlined,
            label: 'Home',
            isActive: false,
            onTap: () => context.go('/dashboard'),
          ),
          _buildNavItem(
            icon: Icons.search,
            label: 'Search',
            isActive: true,
            onTap: () => context.go('/dashboard'),
          ),
          _buildNavItem(
            icon: Icons.calendar_today_outlined,
            label: 'Schedules',
            isActive: false,
            onTap: () => context.go('/dashboard'),
          ),
          _buildNavItem(
            icon: Icons.settings_outlined,
            label: 'Settings',
            isActive: false,
            onTap: () => context.go('/dashboard'),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem({
    required IconData icon,
    required String label,
    required bool isActive,
    required VoidCallback onTap,
  }) {
    final color = isActive ? const Color(0xFF059669) : const Color(0xFF9CA3AF);
    return GestureDetector(
      onTap: onTap,
      behavior: HitTestBehavior.opaque,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 10,
              fontWeight: FontWeight.w500,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }
}
