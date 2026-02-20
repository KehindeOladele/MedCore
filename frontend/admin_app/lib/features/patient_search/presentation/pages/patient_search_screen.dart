import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:go_router/go_router.dart';

class PatientSearchScreen extends StatefulWidget {
  const PatientSearchScreen({super.key});

  @override
  State<PatientSearchScreen> createState() => _PatientSearchScreenState();
}

class _PatientSearchScreenState extends State<PatientSearchScreen> {
  final TextEditingController _searchController = TextEditingController();

  // Simulated backend datastore
  final List<Map<String, String>> _allPatients = [
    {'name': 'Luke Maxwell', 'id': 'MED-882190', 'age': '34 yrs'},
    {'name': 'Sarah Johnson', 'id': 'MED-882191', 'age': '28 yrs'},
    {'name': 'Michael Chen', 'id': 'MED-882192', 'age': '45 yrs'},
  ];

  // Recently consulted list - populate with the dummy data to ensure it displays immediately
  final List<Map<String, String>> _recentConsultees = [
    {'name': 'Luke Maxwell', 'id': 'MED-882190', 'age': '34 yrs'},
  ];

  List<Map<String, String>> _searchResults = [];
  bool _isSearching = false;
  bool _hasUnreadNotifications = true; // Simulating unread notifications state

  @override
  void initState() {
    super.initState();
    _searchController.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    _searchController.removeListener(_onSearchChanged);
    _searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged() {
    final query = _searchController.text.trim().toLowerCase();
    if (query.isEmpty) {
      setState(() {
        _isSearching = false;
        _searchResults = [];
      });
      return;
    }

    // Querying the "backend" for options matching ID or Name
    setState(() {
      _isSearching = true;
      _searchResults = _allPatients.where((patient) {
        final nameMatch = patient['name']!.toLowerCase().contains(query);
        final idMatch = patient['id']!.toLowerCase().contains(query);
        return nameMatch || idMatch;
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 20.h),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 10.h),

              // Doctor Profile Header
              Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: const Color.fromRGBO(5, 150, 105, 0.2),
                        width: 2,
                      ),
                      image: const DecorationImage(
                        image: AssetImage(
                          'assets/images/dr_israel.png',
                        ), // Will need the actual image or placeholder
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  SizedBox(width: 12.w),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Dr. Israel',
                          style: TextStyle(
                            color: const Color(0xFF111827),
                            fontSize: 18.sp,
                            fontWeight: FontWeight.w700,
                            fontFamily: 'Inter',
                          ),
                        ),
                        SizedBox(height: 2.h),
                        Text(
                          'Cardiologist',
                          style: TextStyle(
                            color: const Color(0xFF94A3B8),
                            fontSize: 12.sp,
                            fontWeight: FontWeight.w500,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Notification Bell
                  Container(
                    width: 40,
                    height: 40,
                    decoration: const BoxDecoration(
                      color: Color(0xFFF9FAFB),
                      shape: BoxShape.circle,
                    ),
                    child: Stack(
                      clipBehavior: Clip.none,
                      children: [
                        Center(
                          child: IconButton(
                            onPressed: () {
                              setState(() {
                                // Simulate reading notifications
                                _hasUnreadNotifications = false;
                              });
                            },
                            icon: const Icon(Icons.notifications_none),
                            color: const Color(0xFF64748B),
                            iconSize: 24,
                            padding: EdgeInsets.zero,
                            constraints: const BoxConstraints(),
                          ),
                        ),
                        if (_hasUnreadNotifications)
                          Positioned(
                            right: 10,
                            top: 8,
                            child: Container(
                              width: 8,
                              height: 8,
                              decoration: const BoxDecoration(
                                color: Color(0xFFEF4444),
                                shape: BoxShape.circle,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                ],
              ),

              SizedBox(height: 40.h),

              // Find Patient Title
              Text(
                'Find Patient',
                style: TextStyle(
                  color: const Color(0xFF0F172A),
                  fontSize: 24.sp,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'Inter',
                  letterSpacing: -0.6,
                ),
              ),

              SizedBox(height: 24.h),

              // Search Input Label
              Text(
                'Patient Name or ID',
                style: TextStyle(
                  color: const Color(0xFF6B7280),
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'Inter',
                ),
              ),

              SizedBox(height: 8.h),

              // Search Input Field
              TextField(
                controller: _searchController,
                style: TextStyle(
                  color: const Color(0xFF64748B),
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w500,
                  fontFamily: 'Inter',
                ),
                decoration: InputDecoration(
                  hintText: 'MED-882190',
                  hintStyle: TextStyle(
                    color: const Color(0xFF64748B).withValues(alpha: 0.5),
                    fontSize: 14.sp,
                    fontWeight: FontWeight.w500,
                  ),
                  filled: true,
                  fillColor: Colors.white,
                  contentPadding: EdgeInsets.symmetric(
                    horizontal: 16.w,
                    vertical: 18.h,
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(
                      color: Color(0xFF00A36C),
                      width: 2,
                    ),
                  ),
                ),
              ),

              SizedBox(height: 24.h),

              // Search Button
              SizedBox(
                width: double.infinity,
                height: 50.h,
                child: ElevatedButton(
                  onPressed: _onSearchChanged,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF059669),
                    foregroundColor: Colors.white,
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  ),
                  child: Text(
                    'Search',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ),

              SizedBox(height: 48.h),

              // Section Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    _isSearching ? 'SEARCH RESULTS' : 'RECENTLY CONSULTED',
                    style: TextStyle(
                      color: const Color(0xFF94A3B8),
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                      letterSpacing: 1.8,
                    ),
                  ),
                  if (!_isSearching && _recentConsultees.isNotEmpty)
                    TextButton(
                      onPressed: () {},
                      style: TextButton.styleFrom(
                        padding: EdgeInsets.zero,
                        minimumSize: Size.zero,
                        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      ),
                      child: Text(
                        'View All',
                        style: TextStyle(
                          color: const Color.fromRGBO(19, 236, 91, 0.8),
                          fontSize: 14.sp,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Inter',
                        ),
                      ),
                    ),
                ],
              ),

              SizedBox(height: 16.h),

              // Dynamic List Rendering
              if (_isSearching)
                _searchResults.isEmpty
                    ? _buildEmptyState('No patient found matching your query.')
                    : Column(
                        children: _searchResults
                            .map(
                              (patient) => _buildPatientCard(context, patient),
                            )
                            .toList(),
                      )
              else
                _recentConsultees.isEmpty
                    ? _buildEmptyState('No recent consultee found.')
                    : Column(
                        children: _recentConsultees
                            .map(
                              (patient) => _buildPatientCard(context, patient),
                            )
                            .toList(),
                      ),

              SizedBox(height: 32.h), // Bottom Padding
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState(String message) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(vertical: 48.h),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 64,
            height: 64,
            decoration: const BoxDecoration(
              color: Color(0xFFF8FAFC),
              shape: BoxShape.circle,
            ),
            child: Center(
              child: SvgPicture.asset(
                'assets/icons/user_name.svg',
                width: 24,
                colorFilter: const ColorFilter.mode(
                  Color(0xFF94A3B8),
                  BlendMode.srcIn,
                ),
              ),
            ),
          ),
          SizedBox(height: 16.h),
          Text(
            message,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: const Color(0xFF64748B),
              fontSize: 14.sp,
              fontWeight: FontWeight.w500,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPatientCard(BuildContext context, Map<String, String> patient) {
    return Padding(
      padding: EdgeInsets.only(bottom: 16.h),
      child: InkWell(
        onTap: () {
          context.push('/patient_records');
        },
        borderRadius: BorderRadius.circular(20),
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 10.h),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: const Color(0xFFF8FAFC)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.02),
                blurRadius: 10,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                width: 56,
                height: 56,
                decoration: const BoxDecoration(
                  color: Color.fromRGBO(19, 236, 91, 0.1),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: SvgPicture.asset(
                    'assets/icons/user_name.svg',
                    width: 20,
                    height: 20,
                    colorFilter: const ColorFilter.mode(
                      Color(0xFF059669),
                      BlendMode.srcIn,
                    ),
                  ),
                ),
              ),
              SizedBox(width: 16.w),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      patient['name']!,
                      style: TextStyle(
                        color: const Color(0xFF0F172A),
                        fontSize: 18.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                      ),
                    ),
                    SizedBox(height: 4.h),
                    Text(
                      'ID: ${patient['id']} • ${patient['age']}',
                      style: TextStyle(
                        color: const Color(0xFF64748B),
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w500,
                        fontFamily: 'Inter',
                        letterSpacing: -0.35,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
