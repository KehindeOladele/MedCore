import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../providers/patient_history_provider.dart';

class PatientHistoryScreen extends ConsumerWidget {
  const PatientHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final historyAsync = ref.watch(patientMedicalHistoryProvider);

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
        title: Column(
          children: [
            Text(
              'Medical History',
              style: TextStyle(
                color: const Color(0xFF0F172A),
                fontSize: 18.sp,
                fontWeight: FontWeight.w700,
                fontFamily: 'Inter',
              ),
            ),
            SizedBox(height: 2.h),
            Text(
              'Luke Maxwell • ID: MED-882190',
              style: TextStyle(
                color: const Color(0xFF64748B),
                fontSize: 12.sp,
                fontWeight: FontWeight.w500,
                fontFamily: 'Inter',
              ),
            ),
          ],
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 16.h),
            // Search Bar
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 24.w),
              child: TextField(
                style: TextStyle(
                  color: const Color(0xFF64748B),
                  fontSize: 14.sp,
                  fontWeight: FontWeight.w500,
                  fontFamily: 'Inter',
                ),
                decoration: InputDecoration(
                  hintText: "Search conditions...",
                  hintStyle: TextStyle(
                    color: const Color(0xFF64748B).withValues(alpha: 0.5),
                    fontSize: 14.sp,
                    fontWeight: FontWeight.w500,
                  ),
                  prefixIcon: Icon(
                    Icons.search,
                    color: const Color(0xFF94A3B8),
                    size: 20.sp,
                  ),
                  filled: true,
                  fillColor: Colors.white,
                  contentPadding: EdgeInsets.symmetric(
                    horizontal: 16.w,
                    vertical: 16.h,
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
            ),

            SizedBox(height: 24.h),

            // Timeline List
            Expanded(
              child: historyAsync.when(
                loading: () => const Center(
                  child: CircularProgressIndicator(color: Color(0xFF059669)),
                ),
                error: (err, stack) =>
                    Center(child: Text('Error loading history: $err')),
                data: (historyItems) {
                  if (historyItems.isEmpty) {
                    return const Center(
                      child: Text("No medical history found."),
                    );
                  }

                  return Stack(
                    children: [
                      ListView.builder(
                        padding: EdgeInsets.symmetric(
                          horizontal: 24.w,
                          vertical: 8.h,
                        ),
                        itemCount: historyItems.length,
                        itemBuilder: (context, index) {
                          final item = historyItems[index];
                          bool showHeader =
                              index == 0 ||
                              (historyItems[index].date.month !=
                                  historyItems[index - 1].date.month);

                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (showHeader)
                                Padding(
                                  padding: EdgeInsets.only(
                                    bottom: 16.h,
                                    top: 8.h,
                                  ),
                                  child: Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        _getMonthYear(item.date),
                                        style: TextStyle(
                                          color: const Color(0xFF0F172A),
                                          fontWeight: FontWeight.w700,
                                          fontSize: 16.sp,
                                          fontFamily: 'Inter',
                                          letterSpacing: -0.3,
                                        ),
                                      ),
                                      if (index ==
                                          0) // Only show the add button on the first header
                                        Container(
                                          width: 36,
                                          height: 36,
                                          decoration: BoxDecoration(
                                            color: const Color(0xFF059669),
                                            shape: BoxShape.circle,
                                            boxShadow: [
                                              BoxShadow(
                                                color: const Color(
                                                  0xFF059669,
                                                ).withValues(alpha: 0.3),
                                                blurRadius: 8,
                                                offset: const Offset(0, 4),
                                              ),
                                            ],
                                          ),
                                          child: IconButton(
                                            onPressed: () {},
                                            icon: const Icon(
                                              Icons.add,
                                              color: Colors.white,
                                              size: 20,
                                            ),
                                            padding: EdgeInsets.zero,
                                          ),
                                        ),
                                    ],
                                  ),
                                ),
                              IntrinsicHeight(
                                child: Row(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.stretch,
                                  children: [
                                    // Timeline Indicator
                                    Column(
                                      children: [
                                        Container(
                                          width: 36,
                                          height: 36,
                                          decoration: BoxDecoration(
                                            color: index == 0
                                                ? const Color.fromRGBO(
                                                    5,
                                                    150,
                                                    105,
                                                    0.1,
                                                  )
                                                : const Color(0xFFF1F5F9),
                                            shape: BoxShape.circle,
                                          ),
                                          child: Center(
                                            child: Text(
                                              "${item.date.day}",
                                              style: TextStyle(
                                                color: index == 0
                                                    ? const Color(0xFF059669)
                                                    : const Color(0xFF64748B),
                                                fontWeight: FontWeight.bold,
                                                fontSize: 13.sp,
                                              ),
                                            ),
                                          ),
                                        ),
                                        Expanded(
                                          child: Container(
                                            width: 2,
                                            color: const Color(0xFFE2E8F0),
                                            margin: EdgeInsets.symmetric(
                                              vertical: 4.h,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    SizedBox(width: 16.w),

                                    // Card Content
                                    Expanded(
                                      child: Padding(
                                        padding: EdgeInsets.only(bottom: 24.h),
                                        child: Container(
                                          decoration: BoxDecoration(
                                            color: Colors.white,
                                            borderRadius: BorderRadius.circular(
                                              16,
                                            ),
                                            border: Border.all(
                                              color: const Color(0xFFF1F5F9),
                                            ),
                                            boxShadow: [
                                              BoxShadow(
                                                color: Colors.black.withValues(
                                                  alpha: 0.02,
                                                ),
                                                blurRadius: 8,
                                                offset: const Offset(0, 4),
                                              ),
                                            ],
                                          ),
                                          padding: EdgeInsets.all(16.w),
                                          child: Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Row(
                                                children: [
                                                  Container(
                                                    padding: EdgeInsets.all(
                                                      8.w,
                                                    ),
                                                    decoration: BoxDecoration(
                                                      color:
                                                          item.type ==
                                                              'pharmacy'
                                                          ? const Color(
                                                              0xFFE0F7FA,
                                                            )
                                                          : const Color(
                                                              0xFFE8F5E9,
                                                            ),
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                            8,
                                                          ),
                                                    ),
                                                    child: Icon(
                                                      item.type == 'pharmacy'
                                                          ? Icons
                                                                .assignment_outlined
                                                          : Icons
                                                                .local_hospital_outlined,
                                                      color:
                                                          item.type ==
                                                              'pharmacy'
                                                          ? const Color(
                                                              0xFF00BCD4,
                                                            )
                                                          : const Color(
                                                              0xFF4CAF50,
                                                            ),
                                                      size: 20,
                                                    ),
                                                  ),
                                                  SizedBox(width: 12.w),
                                                  Expanded(
                                                    child: Column(
                                                      crossAxisAlignment:
                                                          CrossAxisAlignment
                                                              .start,
                                                      children: [
                                                        Text(
                                                          item.title,
                                                          style: TextStyle(
                                                            color: const Color(
                                                              0xFF0F172A,
                                                            ),
                                                            fontWeight:
                                                                FontWeight.w700,
                                                            fontSize: 14.sp,
                                                            fontFamily: 'Inter',
                                                          ),
                                                        ),
                                                        Text(
                                                          item.subtitle,
                                                          style: TextStyle(
                                                            color: const Color(
                                                              0xFF94A3B8,
                                                            ),
                                                            fontSize: 12.sp,
                                                            fontFamily: 'Inter',
                                                          ),
                                                        ),
                                                      ],
                                                    ),
                                                  ),
                                                ],
                                              ),
                                              SizedBox(height: 12.h),
                                              Text(
                                                item.description,
                                                style: TextStyle(
                                                  color: const Color(
                                                    0xFF475569,
                                                  ),
                                                  fontSize: 13.sp,
                                                  height: 1.5,
                                                  fontFamily: 'Inter',
                                                ),
                                              ),
                                              if (item.actionText != null) ...[
                                                SizedBox(height: 16.h),
                                                SizedBox(
                                                  width: double.infinity,
                                                  child: TextButton.icon(
                                                    onPressed: () {},
                                                    icon: Icon(
                                                      item.actionText!.contains(
                                                            "LAB",
                                                          )
                                                          ? Icons
                                                                .description_outlined
                                                          : Icons
                                                                .calendar_view_day_outlined,
                                                      size: 16.sp,
                                                      color: const Color(
                                                        0xFF059669,
                                                      ),
                                                    ),
                                                    label: Text(
                                                      item.actionText!,
                                                      style: TextStyle(
                                                        fontWeight:
                                                            FontWeight.w700,
                                                        fontSize: 12.sp,
                                                        color: const Color(
                                                          0xFF059669,
                                                        ),
                                                        letterSpacing: 0.5,
                                                      ),
                                                    ),
                                                    style: TextButton.styleFrom(
                                                      backgroundColor:
                                                          const Color.fromRGBO(
                                                            5,
                                                            150,
                                                            105,
                                                            0.08,
                                                          ),
                                                      shape: RoundedRectangleBorder(
                                                        borderRadius:
                                                            BorderRadius.circular(
                                                              8,
                                                            ),
                                                      ),
                                                      padding:
                                                          EdgeInsets.symmetric(
                                                            vertical: 10.h,
                                                          ),
                                                    ),
                                                  ),
                                                ),
                                              ],
                                            ],
                                          ),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          );
                        },
                      ),

                      // View Medical Record Bottom Button
                      Positioned(
                        left: 24.w,
                        right: 24.w,
                        bottom: 32.h,
                        child: SizedBox(
                          width: double.infinity,
                          height: 56.h,
                          child: ElevatedButton.icon(
                            onPressed: () {},
                            icon: const Icon(
                              Icons.assignment,
                              color: Colors.white,
                              size: 20,
                            ),
                            label: Text(
                              "View Medical Record",
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16.sp,
                              ),
                            ),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF059669),
                              foregroundColor: Colors.white,
                              elevation: 0,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(28),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getMonthYear(DateTime date) {
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    return "${months[date.month - 1]} ${date.year}";
  }
}
