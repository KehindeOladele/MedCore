import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/patient_models.dart';
import '../providers/patient_controller.dart';

class PatientSearchScreen extends ConsumerStatefulWidget {
  const PatientSearchScreen({super.key});

  @override
  ConsumerState<PatientSearchScreen> createState() => _PatientSearchScreenState();
}

class _PatientSearchScreenState extends ConsumerState<PatientSearchScreen> {
  final TextEditingController _searchController = TextEditingController();

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
    setState(() {}); // rebuilds to show/hide the search section header
  }

  void _triggerSearch() {
    final query = _searchController.text.trim();
    ref.read(patientControllerProvider.notifier).search(query);
  }

  @override
  Widget build(BuildContext context) {
    final isSearching = _searchController.text.trim().isNotEmpty;
    
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
                  onPressed: _triggerSearch,
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
                    isSearching ? 'SEARCH RESULTS' : 'SEARCH HISTORY',
                    style: TextStyle(
                      color: const Color(0xFF94A3B8),
                      fontSize: 12.sp,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'Inter',
                      letterSpacing: 1.8,
                    ),
                  ),
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
              Builder(builder: (context) {
                final patientsAsync = ref.watch(patientControllerProvider);

                // Idle state — no search performed yet
                if (patientsAsync is AsyncData &&
                    patientsAsync.value == null) {
                  return _buildIdleState();
                }

                return patientsAsync.when(
                  loading: () => Center(
                    child: Padding(
                      padding: EdgeInsets.only(top: 40.h),
                      child: const CircularProgressIndicator(
                          color: Color(0xFF059669)),
                    ),
                  ),
                  error: (error, _) =>
                      _buildEmptyState('Something went wrong.\nPlease try again.'),
                  data: (patients) {
                    final list = patients ?? [];
                    if (list.isEmpty) {
                      return _buildEmptyState(
                          'No patient found matching your query.');
                    }
                    return Column(
                      children: list
                          .map((p) => _buildPatientCard(context, p))
                          .toList(),
                    );
                  },
                );
              }),

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

  Widget _buildIdleState() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(vertical: 56.h),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 72,
            height: 72,
            decoration: const BoxDecoration(
              color: Color(0xFFF0FDF4),
              shape: BoxShape.circle,
            ),
            child: const Center(
              child: Icon(
                Icons.search_rounded,
                color: Color(0xFF059669),
                size: 32,
              ),
            ),
          ),
          SizedBox(height: 16.h),
          Text(
            'No search history',
            style: TextStyle(
              color: const Color(0xFF0F172A),
              fontSize: 15.sp,
              fontWeight: FontWeight.w600,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 6.h),
          Text(
            'Enter a patient name or ID\nand tap Search',
            textAlign: TextAlign.center,
            style: TextStyle(
              color: const Color(0xFF94A3B8),
              fontSize: 13.sp,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPatientCard(BuildContext context, Patient patient) {
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
                      patient.fullName,
                      style: TextStyle(
                        color: const Color(0xFF0F172A),
                        fontSize: 18.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                      ),
                    ),
                    SizedBox(height: 4.h),
                    Text(
                      'ID: ${patient.id} • ${patient.age}',
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
