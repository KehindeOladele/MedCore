import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../../../patient_search/presentation/pages/patient_search_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0;

  final List<Widget> _pages = [
    const PatientSearchScreen(),
    const _SchedulesTab(),
    const _SettingsTab(),
  ];

  void _onTabTapped(int index) {
    setState(() {
      _currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex],
      bottomNavigationBar: Container(
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
            _buildNavItem(0, 'Search', 'assets/icons/search.svg'),
            _buildNavItem(1, 'Schedules', 'assets/icons/calendar.svg'),
            _buildNavItem(2, 'Settings', 'assets/icons/settings.svg'),
          ],
        ),
      ),
    );
  }

  Widget _buildNavItem(int index, String label, String iconPath) {
    final isSelected = _currentIndex == index;
    final color = isSelected
        ? const Color(0xFF059669)
        : const Color(0xFF9CA3AF);

    return GestureDetector(
      onTap: () => _onTabTapped(index),
      behavior: HitTestBehavior.opaque,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SvgPicture.asset(
            iconPath,
            width: 24,
            height: 24,
            colorFilter: ColorFilter.mode(color, BlendMode.srcIn),
          ),
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

// ─────────────────────────────────────────────────────────────────────────────
// SCHEDULES TAB
// ─────────────────────────────────────────────────────────────────────────────

class _SchedulesTab extends StatefulWidget {
  const _SchedulesTab();

  @override
  State<_SchedulesTab> createState() => _SchedulesTabState();
}

class _SchedulesTabState extends State<_SchedulesTab> {
  int _selectedDay = 0; // 0 = today

  final List<Map<String, dynamic>> _week = [
    {'label': 'Mon', 'day': '17'},
    {'label': 'Tue', 'day': '18'},
    {'label': 'Wed', 'day': '19'},
    {'label': 'Thu', 'day': '20'},
    {'label': 'Fri', 'day': '21'},
    {'label': 'Sat', 'day': '22'},
    {'label': 'Sun', 'day': '23'},
  ];

  final List<Map<String, dynamic>> _appointments = [
    {
      'time': '08:30 AM',
      'duration': '30 min',
      'patient': 'Luke Maxwell',
      'id': 'MED-882190',
      'type': 'Follow-up',
      'color': const Color(0xFF059669),
      'bg': const Color(0xFFECFDF5),
    },
    {
      'time': '10:00 AM',
      'duration': '45 min',
      'patient': 'Sarah Johnson',
      'id': 'MED-882191',
      'type': 'Consultation',
      'color': const Color(0xFF3B82F6),
      'bg': const Color(0xFFEFF6FF),
    },
    {
      'time': '11:30 AM',
      'duration': '20 min',
      'patient': 'Michael Chen',
      'id': 'MED-882192',
      'type': 'Lab Review',
      'color': const Color(0xFF8B5CF6),
      'bg': const Color(0xFFF5F3FF),
    },
    {
      'time': '02:00 PM',
      'duration': '60 min',
      'patient': 'Amara Okafor',
      'id': 'MED-882194',
      'type': 'New Patient',
      'color': const Color(0xFFEF4444),
      'bg': const Color(0xFFFEF2F2),
    },
    {
      'time': '03:45 PM',
      'duration': '30 min',
      'patient': 'James Adeleke',
      'id': 'MED-882195',
      'type': 'Follow-up',
      'color': const Color(0xFF059669),
      'bg': const Color(0xFFECFDF5),
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Padding(
              padding: EdgeInsets.fromLTRB(24.w, 20.h, 24.w, 0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Schedule',
                        style: TextStyle(
                          color: const Color(0xFF0F172A),
                          fontSize: 24.sp,
                          fontWeight: FontWeight.w700,
                          fontFamily: 'Inter',
                          letterSpacing: -0.5,
                        ),
                      ),
                      SizedBox(height: 4.h),
                      Text(
                        'Feb 2026 • ${_appointments.length} appointments',
                        style: TextStyle(
                          color: const Color(0xFF64748B),
                          fontSize: 13.sp,
                          fontFamily: 'Inter',
                        ),
                      ),
                    ],
                  ),
                  Container(
                    width: 40,
                    height: 40,
                    decoration: const BoxDecoration(
                      color: Color(0xFF059669),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.add, color: Colors.white, size: 22),
                  ),
                ],
              ),
            ),

            SizedBox(height: 24.h),

            // Horizontal day picker
            SizedBox(
              height: 72.h,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: EdgeInsets.symmetric(horizontal: 20.w),
                itemCount: _week.length,
                itemBuilder: (context, i) {
                  final isSelected = _selectedDay == i;
                  return GestureDetector(
                    onTap: () => setState(() => _selectedDay = i),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      margin: EdgeInsets.only(right: 8.w),
                      width: 52.w,
                      decoration: BoxDecoration(
                        color: isSelected
                            ? const Color(0xFF059669)
                            : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isSelected
                              ? const Color(0xFF059669)
                              : const Color(0xFFE2E8F0),
                        ),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            _week[i]['label']!,
                            style: TextStyle(
                              color: isSelected
                                  ? Colors.white.withValues(alpha: 0.8)
                                  : const Color(0xFF94A3B8),
                              fontSize: 11.sp,
                              fontWeight: FontWeight.w500,
                              fontFamily: 'Inter',
                            ),
                          ),
                          SizedBox(height: 4.h),
                          Text(
                            _week[i]['day']!,
                            style: TextStyle(
                              color: isSelected
                                  ? Colors.white
                                  : const Color(0xFF0F172A),
                              fontSize: 18.sp,
                              fontWeight: FontWeight.w700,
                              fontFamily: 'Inter',
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),

            SizedBox(height: 24.h),

            Padding(
              padding: EdgeInsets.symmetric(horizontal: 24.w),
              child: Text(
                'TODAY\'S APPOINTMENTS',
                style: TextStyle(
                  color: const Color(0xFF94A3B8),
                  fontSize: 11.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.4,
                  fontFamily: 'Inter',
                ),
              ),
            ),

            SizedBox(height: 16.h),

            // Appointment list
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.symmetric(horizontal: 24.w),
                itemCount: _appointments.length,
                itemBuilder: (context, i) =>
                    _buildAppointmentCard(_appointments[i]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAppointmentCard(Map<String, dynamic> appt) {
    return Padding(
      padding: EdgeInsets.only(bottom: 16.h),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Time column
          SizedBox(
            width: 72.w,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  appt['time'].toString().split(' ')[0],
                  style: TextStyle(
                    color: const Color(0xFF0F172A),
                    fontSize: 14.sp,
                    fontWeight: FontWeight.w700,
                    fontFamily: 'Inter',
                  ),
                ),
                Text(
                  appt['time'].toString().split(' ')[1],
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 11.sp,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 4.h),
                Text(
                  appt['duration'],
                  style: TextStyle(
                    color: const Color(0xFF94A3B8),
                    fontSize: 10.sp,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),

          SizedBox(width: 12.w),

          // Left accent bar
          Container(
            width: 4,
            height: 80.h,
            decoration: BoxDecoration(
              color: appt['color'] as Color,
              borderRadius: BorderRadius.circular(2),
            ),
          ),

          SizedBox(width: 12.w),

          // Card
          Expanded(
            child: Container(
              padding: EdgeInsets.all(16.w),
              decoration: BoxDecoration(
                color: appt['bg'] as Color,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          appt['patient'],
                          style: TextStyle(
                            color: const Color(0xFF0F172A),
                            fontSize: 15.sp,
                            fontWeight: FontWeight.w700,
                            fontFamily: 'Inter',
                          ),
                        ),
                        SizedBox(height: 4.h),
                        Text(
                          'ID: ${appt['id']}',
                          style: TextStyle(
                            color: const Color(0xFF64748B),
                            fontSize: 12.sp,
                            fontFamily: 'Inter',
                          ),
                        ),
                        SizedBox(height: 8.h),
                        Container(
                          padding: EdgeInsets.symmetric(
                            horizontal: 10.w,
                            vertical: 3.h,
                          ),
                          decoration: BoxDecoration(
                            color: (appt['color'] as Color).withValues(
                              alpha: 0.15,
                            ),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            appt['type'],
                            style: TextStyle(
                              color: appt['color'] as Color,
                              fontSize: 11.sp,
                              fontWeight: FontWeight.w600,
                              fontFamily: 'Inter',
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Icon(
                    Icons.chevron_right_rounded,
                    color: const Color(0xFF94A3B8),
                    size: 20.sp,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// SETTINGS TAB
// ─────────────────────────────────────────────────────────────────────────────

class _SettingsTab extends StatelessWidget {
  const _SettingsTab();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            children: [
              // Profile header
              _buildProfileHeader(),

              SizedBox(height: 24.h),

              // Settings groups
              _buildSectionLabel('PREFERENCES'),
              _buildSettingsTile(
                icon: Icons.notifications_outlined,
                iconColor: const Color(0xFF059669),
                iconBg: const Color(0xFFECFDF5),
                title: 'Notifications',
                subtitle: 'Manage alerts and reminders',
                trailing: Switch(
                  value: true,
                  onChanged: (_) {},
                  activeThumbColor: const Color(0xFF059669),
                ),
              ),
              _buildDivider(),
              _buildSettingsTile(
                icon: Icons.language_outlined,
                iconColor: const Color(0xFF3B82F6),
                iconBg: const Color(0xFFEFF6FF),
                title: 'Language',
                subtitle: 'English (US)',
              ),
              _buildDivider(),
              _buildSettingsTile(
                icon: Icons.dark_mode_outlined,
                iconColor: const Color(0xFF8B5CF6),
                iconBg: const Color(0xFFF5F3FF),
                title: 'Appearance',
                subtitle: 'Light mode',
              ),

              SizedBox(height: 8.h),
              _buildSectionLabel('SECURITY & PRIVACY'),
              _buildSettingsTile(
                icon: Icons.lock_outline_rounded,
                iconColor: const Color(0xFFD97706),
                iconBg: const Color(0xFFFFFBEB),
                title: 'Security',
                subtitle: 'PIN, biometrics',
              ),
              _buildDivider(),
              _buildSettingsTile(
                icon: Icons.shield_outlined,
                iconColor: const Color(0xFFEF4444),
                iconBg: const Color(0xFFFEF2F2),
                title: 'Privacy',
                subtitle: 'Data sharing & permissions',
              ),

              SizedBox(height: 8.h),
              _buildSectionLabel('SUPPORT'),
              _buildSettingsTile(
                icon: Icons.help_outline_rounded,
                iconColor: const Color(0xFF64748B),
                iconBg: const Color(0xFFF1F5F9),
                title: 'Help & Support',
                subtitle: 'FAQs, contact us',
              ),
              _buildDivider(),
              _buildSettingsTile(
                icon: Icons.info_outline_rounded,
                iconColor: const Color(0xFF64748B),
                iconBg: const Color(0xFFF1F5F9),
                title: 'About MedCore',
                subtitle: 'Version 1.0.0',
              ),

              SizedBox(height: 8.h),

              // Logout
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 8.h),
                child: SizedBox(
                  width: double.infinity,
                  height: 52.h,
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(
                      Icons.logout_rounded,
                      color: Color(0xFFEF4444),
                    ),
                    label: Text(
                      'Log Out',
                      style: TextStyle(
                        color: const Color(0xFFEF4444),
                        fontSize: 15.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                      ),
                    ),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Color(0xFFFECACA)),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      backgroundColor: const Color(0xFFFEF2F2),
                    ),
                  ),
                ),
              ),

              SizedBox(height: 24.h),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProfileHeader() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.fromLTRB(24.w, 28.h, 24.w, 28.h),
      decoration: const BoxDecoration(color: Colors.white),
      child: Row(
        children: [
          Container(
            width: 68,
            height: 68,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                color: const Color(0xFF059669).withValues(alpha: 0.3),
                width: 2.5,
              ),
              image: const DecorationImage(
                image: AssetImage('assets/images/dr_israel.png'),
                fit: BoxFit.cover,
              ),
              color: const Color(0xFFE2E8F0),
            ),
          ),
          SizedBox(width: 16.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Dr. Israel',
                  style: TextStyle(
                    color: const Color(0xFF0F172A),
                    fontSize: 20.sp,
                    fontWeight: FontWeight.w700,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 2.h),
                Text(
                  'Cardiologist • General Hospital',
                  style: TextStyle(
                    color: const Color(0xFF64748B),
                    fontSize: 13.sp,
                    fontFamily: 'Inter',
                  ),
                ),
                SizedBox(height: 8.h),
                Container(
                  padding: EdgeInsets.symmetric(
                    horizontal: 12.w,
                    vertical: 4.h,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFECFDF5),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    'Active',
                    style: TextStyle(
                      color: const Color(0xFF059669),
                      fontSize: 11.sp,
                      fontWeight: FontWeight.w600,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ],
            ),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(
              Icons.edit_outlined,
              color: Color(0xFF64748B),
              size: 20,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionLabel(String label) {
    return Padding(
      padding: EdgeInsets.fromLTRB(24.w, 16.h, 24.w, 8.h),
      child: Text(
        label,
        style: TextStyle(
          color: const Color(0xFF94A3B8),
          fontSize: 11.sp,
          fontWeight: FontWeight.w700,
          letterSpacing: 1.4,
          fontFamily: 'Inter',
        ),
      ),
    );
  }

  Widget _buildSettingsTile({
    required IconData icon,
    required Color iconColor,
    required Color iconBg,
    required String title,
    required String subtitle,
    Widget? trailing,
  }) {
    return Container(
      color: Colors.white,
      child: ListTile(
        contentPadding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 4.h),
        leading: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: iconBg,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: iconColor, size: 20),
        ),
        title: Text(
          title,
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 14.sp,
            fontWeight: FontWeight.w600,
            fontFamily: 'Inter',
          ),
        ),
        subtitle: Text(
          subtitle,
          style: TextStyle(
            color: const Color(0xFF94A3B8),
            fontSize: 12.sp,
            fontFamily: 'Inter',
          ),
        ),
        trailing:
            trailing ??
            const Icon(
              Icons.chevron_right_rounded,
              color: Color(0xFFCBD5E1),
              size: 20,
            ),
        onTap: () {},
      ),
    );
  }

  Widget _buildDivider() {
    return Container(
      color: Colors.white,
      child: Padding(
        padding: EdgeInsets.only(left: 80.w),
        child: const Divider(height: 1, color: Color(0xFFF1F5F9)),
      ),
    );
  }
}
