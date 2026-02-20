import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../../../patient_search/presentation/pages/patient_search_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0; // 0 is now Search, 1 is Schedules, 2 is Settings

  final List<Widget> _pages = [
    const PatientSearchScreen(),
    const Center(child: Text('Schedules')),
    const Center(child: Text('Settings')),
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
            _buildNavItem(
              0, // Maps to Search
              'Search',
              'assets/icons/search.svg',
              'assets/icons/search.svg', // Assuming search svg has no pure filled variant, but coloring handles it
            ),
            _buildNavItem(
              1, // Maps to Schedules
              'Schedules',
              'assets/icons/calendar.svg',
              'assets/icons/calendar.svg',
            ),
            _buildNavItem(
              2, // Maps to Settings
              'Settings',
              'assets/icons/settings.svg',
              'assets/icons/settings.svg',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNavItem(
    int index,
    String label,
    String iconPath,
    String activeIconPath,
  ) {
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
            isSelected ? activeIconPath : iconPath,
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
