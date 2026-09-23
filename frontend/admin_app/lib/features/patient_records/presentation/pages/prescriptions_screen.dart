import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../../data/models/prescription_model.dart';

class PrescriptionsScreen extends StatelessWidget {
  const PrescriptionsScreen({super.key});

  static const _green = Color(0xFF059669);

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
          _buildTabBar(context),
          Expanded(
            // ValueListenableBuilder updates automatically when store changes
            child: ValueListenableBuilder<List<PrescriptionModel>>(
              valueListenable: PrescriptionStore.instance.prescriptions,
              builder: (context, prescriptions, _) {
                final ongoing = prescriptions
                    .where((p) => !p.isCompleted)
                    .toList();
                final completed = prescriptions
                    .where((p) => p.isCompleted)
                    .toList();

                if (prescriptions.isEmpty) {
                  return _buildEmptyState(context);
                }

                return SingleChildScrollView(
                  padding: EdgeInsets.symmetric(
                    horizontal: 20.w,
                    vertical: 20.h,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (ongoing.isNotEmpty) ...[
                        _sectionLabel('ONGOING PRESCRIPTION'),
                        SizedBox(height: 12.h),
                        ...ongoing.map(
                          (p) => Padding(
                            padding: EdgeInsets.only(bottom: 12.h),
                            child: _prescriptionCard(context, p),
                          ),
                        ),
                        SizedBox(height: 16.h),
                      ],
                      if (completed.isNotEmpty) ...[
                        _sectionLabel('COMPLETED'),
                        SizedBox(height: 12.h),
                        ...completed.map(
                          (p) => Padding(
                            padding: EdgeInsets.only(bottom: 12.h),
                            child: _prescriptionCard(context, p),
                          ),
                        ),
                      ],
                      SizedBox(height: 100.h),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.push('/add_prescription'),
        backgroundColor: _green,
        elevation: 3,
        child: const Icon(Icons.add, color: Colors.white, size: 28),
      ),
      bottomNavigationBar: _buildBottomNav(context),
    );
  }

  // ─── EMPTY STATE ──────────────────────────────────────────────────────────
  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 80.w,
            height: 80.w,
            decoration: BoxDecoration(
              color: const Color(0xFFECFDF5),
              shape: BoxShape.circle,
            ),
            child: Icon(Icons.medication_outlined, color: _green, size: 40),
          ),
          SizedBox(height: 20.h),
          Text(
            'No Prescriptions Yet',
            style: TextStyle(
              color: const Color(0xFF0F172A),
              fontSize: 18.sp,
              fontWeight: FontWeight.w700,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 8.h),
          Text(
            'Tap + to add a new prescription',
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

  // ─── TAB BAR ──────────────────────────────────────────────────────────────
  Widget _buildTabBar(BuildContext context) {
    final tabs = ['Lab Tests', 'Imaging', 'Notes', 'Prescriptions'];
    const selectedIndex = 3;
    return Container(
      height: 48.h,
      color: Colors.white,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.symmetric(horizontal: 16.w),
        itemCount: tabs.length,
        itemBuilder: (context, index) {
          final isSelected = index == selectedIndex;
          return GestureDetector(
            onTap: () {
              if (index == 0) context.pop();
              if (index == 2) context.push('/clinical_notes');
            },
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 18.w, vertical: 8.h),
              margin: EdgeInsets.only(right: 8.w, top: 6.h, bottom: 6.h),
              decoration: BoxDecoration(
                color: isSelected ? _green : Colors.white,
                borderRadius: BorderRadius.circular(20),
                border: isSelected
                    ? null
                    : Border.all(color: const Color(0xFFE2E8F0)),
              ),
              child: Center(
                child: Text(
                  tabs[index],
                  style: TextStyle(
                    color: isSelected ? Colors.white : const Color(0xFF64748B),
                    fontSize: 13.sp,
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

  // ─── SECTION LABEL ────────────────────────────────────────────────────────
  Widget _sectionLabel(String label) {
    return Text(
      label,
      style: TextStyle(
        color: const Color(0xFF64748B),
        fontSize: 11.sp,
        fontWeight: FontWeight.w700,
        letterSpacing: 1.1,
        fontFamily: 'Inter',
      ),
    );
  }

  // ─── PRESCRIPTION CARD ────────────────────────────────────────────────────
  Widget _prescriptionCard(BuildContext context, PrescriptionModel p) {
    final status = p.statusLabel;

    Color statusBg;
    Color statusText;
    Color iconBg;
    Color iconColor;
    Color infoColor;

    switch (status) {
      case 'Active':
        statusBg = const Color(0xFFD1FAE5);
        statusText = _green;
        iconBg = const Color(0xFFEFF6FF);
        iconColor = const Color(0xFF3B82F6);
        infoColor = const Color(0xFF64748B);
        break;
      case 'Refill Soon':
        statusBg = const Color(0xFFFEE2E2);
        statusText = const Color(0xFFDC2626);
        iconBg = const Color(0xFFF0FDF4);
        iconColor = _green;
        infoColor = const Color(0xFFDC2626);
        break;
      default: // Completed
        statusBg = const Color(0xFFF1F5F9);
        statusText = const Color(0xFF64748B);
        iconBg = const Color(0xFFF8FAFC);
        iconColor = const Color(0xFF94A3B8);
        infoColor = const Color(0xFF94A3B8);
    }

    return GestureDetector(
      onTap: () => context.push('/add_prescription', extra: p),
      child: Container(
        padding: EdgeInsets.all(16.w),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
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
          children: [
            Container(
              width: 44.w,
              height: 44.w,
              decoration: BoxDecoration(
                color: iconBg,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                Icons.medication_outlined,
                color: iconColor,
                size: 22,
              ),
            ),
            SizedBox(width: 14.w),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    p.name,
                    style: TextStyle(
                      color: const Color(0xFF0F172A),
                      fontSize: 15.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                    ),
                  ),
                  SizedBox(height: 2.h),
                  Text(
                    '${p.dosage} • ${p.frequency}',
                    style: TextStyle(
                      color: const Color(0xFF64748B),
                      fontSize: 12.sp,
                      fontFamily: 'Inter',
                    ),
                  ),
                  SizedBox(height: 2.h),
                  Text(
                    p.infoLine,
                    style: TextStyle(
                      color: infoColor,
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w500,
                      fontFamily: 'Inter',
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 10.w, vertical: 5.h),
              decoration: BoxDecoration(
                color: statusBg,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                status,
                style: TextStyle(
                  color: statusText,
                  fontSize: 11.sp,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Inter',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ─── BOTTOM NAV ───────────────────────────────────────────────────────────
  Widget _buildBottomNav(BuildContext context) {
    return Container(
      height: 68,
      decoration: BoxDecoration(
        color: Colors.white,
        border: const Border(top: BorderSide(color: Color(0xFFE5E7EB))),
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
          _navItem(
            Icons.home_outlined,
            'Home',
            false,
            () => context.go('/dashboard'),
          ),
          _navItem(
            Icons.search,
            'Search',
            true,
            () => context.go('/dashboard'),
          ),
          _navItem(
            Icons.calendar_today_outlined,
            'Schedules',
            false,
            () => context.go('/dashboard'),
          ),
          _navItem(
            Icons.settings_outlined,
            'Settings',
            false,
            () => context.go('/dashboard'),
          ),
        ],
      ),
    );
  }

  Widget _navItem(
    IconData icon,
    String label,
    bool active,
    VoidCallback onTap,
  ) {
    final color = active ? _green : const Color(0xFF9CA3AF);
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
            style: TextStyle(color: color, fontSize: 10, fontFamily: 'Inter'),
          ),
        ],
      ),
    );
  }
}
