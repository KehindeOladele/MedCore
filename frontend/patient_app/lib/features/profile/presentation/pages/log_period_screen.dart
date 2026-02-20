import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../../data/models/menstrual_cycle_model.dart';
import '../providers/menstrual_cycle_provider.dart';

class LogPeriodScreen extends ConsumerStatefulWidget {
  const LogPeriodScreen({super.key});

  @override
  ConsumerState<LogPeriodScreen> createState() => _LogPeriodScreenState();
}

class _LogPeriodScreenState extends ConsumerState<LogPeriodScreen> {
  DateTime _focusedMonth = DateTime(
    DateTime.now().year,
    DateTime.now().month,
    1,
  );
  DateTime? _startDate;

  Set<DateTime> get _periodDays {
    if (_startDate == null) return {};
    return List.generate(
      _periodLength,
      (index) => _startDate!.add(Duration(days: index)),
    ).toSet();
  }

  int _periodLength = 5;
  int _cycleLength = 28;
  String _flowIntensity = 'Medium';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final cycleAsync = ref.read(menstrualCycleProvider);
      if (cycleAsync.hasValue && cycleAsync.value != null) {
        final cycle = cycleAsync.value!;
        setState(() {
          _startDate = cycle.lastPeriodDate;
          _periodLength = cycle.periodLength;
          _cycleLength = cycle.cycleLength;
          _flowIntensity = cycle.flowIntensity;
          _focusedMonth = DateTime(
            cycle.lastPeriodDate.year,
            cycle.lastPeriodDate.month,
            1,
          );
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          "Log Your Period",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  const Text(
                    "When did your period start?",
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF1A1C1E),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    "Select the first day of your menstrual flow",
                    style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                  ),
                  const SizedBox(height: 24),

                  // Calendar Card
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.05),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        // Month Header
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.chevron_left),
                              onPressed: () {
                                setState(() {
                                  _focusedMonth = DateTime(
                                    _focusedMonth.year,
                                    _focusedMonth.month - 1,
                                  );
                                });
                              },
                            ),
                            Text(
                              "${_monthName(_focusedMonth.month)} ${_focusedMonth.year}",
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.chevron_right),
                              onPressed: () {
                                setState(() {
                                  _focusedMonth = DateTime(
                                    _focusedMonth.year,
                                    _focusedMonth.month + 1,
                                  );
                                });
                              },
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),

                        // Days Header
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
                              .map(
                                (day) => SizedBox(
                                  width: 32,
                                  child: Center(
                                    child: Text(
                                      day,
                                      style: TextStyle(
                                        color: Colors.grey[500],
                                        fontWeight: FontWeight.w500,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ),
                                ),
                              )
                              .toList(),
                        ),
                        const SizedBox(height: 8),

                        // Days Grid
                        _buildCalendarGrid(),

                        const SizedBox(height: 24),
                        // Legend
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            _buildLegendItem(
                              const Color(0xFFFF5252),
                              "Period Days",
                              isFilled: true,
                            ),
                            const SizedBox(width: 24),
                            _buildLegendItem(
                              Colors.grey,
                              "Today",
                              isFilled: false,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Period Details Card
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.05),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Period Details",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 24),

                        _buildCounterRow(
                          "Period Length (Days)",
                          _periodLength,
                          (val) => setState(() => _periodLength = val),
                          Icons.schedule,
                        ),
                        const SizedBox(height: 24),

                        _buildCounterRow(
                          "Average Cycle Length (Days)",
                          _cycleLength,
                          (val) => setState(() => _cycleLength = val),
                          Icons.calendar_today_outlined,
                        ),
                        const SizedBox(height: 24),

                        // Flow Intensity
                        Row(
                          children: [
                            const Icon(
                              Icons.water_drop_outlined,
                              size: 18,
                              color: AppColors.primary,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              "Flow Intensity",
                              style: TextStyle(
                                fontSize: 13,
                                color: Colors.grey[700],
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.all(4),
                          decoration: BoxDecoration(
                            color: Colors.grey[100],
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            children: [
                              _buildFlowOption("Light"),
                              _buildFlowOption("Medium"),
                              _buildFlowOption("Heavy"),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 100), // Bottom padding
                ],
              ),
            ),
          ),

          // Bottom Button
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(
                top: BorderSide(color: Colors.grey.withOpacity(0.1)),
              ),
            ),
            child: SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: () async {
                  if (_startDate == null) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Please select a start date'),
                      ),
                    );
                    return;
                  }

                  final cycle = MenstrualCycleModel(
                    lastPeriodDate: _startDate!,
                    periodLength: _periodLength,
                    cycleLength: _cycleLength,
                    flowIntensity: _flowIntensity,
                  );

                  await ref
                      .read(menstrualCycleProvider.notifier)
                      .saveCycle(cycle);
                  if (context.mounted) {
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Period details saved!')),
                    );
                  }
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF009688),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 0,
                ),
                child: const Text(
                  "Save Period Information",
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCalendarGrid() {
    final daysInMonth = DateUtils.getDaysInMonth(
      _focusedMonth.year,
      _focusedMonth.month,
    );
    final firstDayOfWeek = DateTime(
      _focusedMonth.year,
      _focusedMonth.month,
      1,
    ).weekday;
    // Adjust to 0-based index where Sunday is 0 for Grid
    final offset = firstDayOfWeek == 7 ? 0 : firstDayOfWeek;

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 7,
        mainAxisSpacing: 4,
        crossAxisSpacing: 4,
        childAspectRatio: 0.85, // Slightly taller than wide
      ),
      itemCount: daysInMonth + offset,
      itemBuilder: (context, index) {
        if (index < offset) return const SizedBox();

        final day = index - offset + 1;
        final date = DateTime(_focusedMonth.year, _focusedMonth.month, day);

        final isToday = DateUtils.isSameDay(date, DateTime.now());
        final isPeriodDay = _periodDays.any(
          (d) => DateUtils.isSameDay(d, date),
        );

        int? cycleDay;
        Color cycleDayColor = Colors.transparent;

        if (_startDate != null) {
          final diff = date.difference(_startDate!).inDays;
          // Calculate cycle day relative to start date (Day 1)
          // Mathematical modulo to handle negative numbers correctly for "days before"
          // We want ... 27, 28, 1, 2, 3 ...
          // If diff is 0, day is 1.
          // If diff is -1, day is 28 (if cycle is 28).

          int effectiveCycleDay = (diff % _cycleLength) + 1;
          cycleDay = effectiveCycleDay;

          // Dynamic Phase Colors
          final ovulationStart = _cycleLength - 14;
          final ovulationEnd =
              ovulationStart +
              2; // User requested 3 days (14, 15, 16 for 28 day cycle)

          if (cycleDay <= _periodLength) {
            cycleDayColor = const Color(0xFFFF5252); // Red (Period)
          } else if (cycleDay < ovulationStart) {
            cycleDayColor = Colors.blue; // Follicular (Blue)
          } else if (cycleDay <= ovulationEnd) {
            cycleDayColor = const Color(0xFF00C853); // Green (Ovulation)
          } else {
            cycleDayColor = Colors.black87; // Luteal (Black)
          }
        }

        return GestureDetector(
          onTap: () {
            setState(() {
              _startDate = date;
            });
          },
          child: Container(
            // Explicitly defined margin/decoration for the cell if needed,
            // but here we rely on the grid delegate.
            // Using proper stacking to avoid interference.
            color: Colors.transparent, // Hit test target
            child: Stack(
              children: [
                // 1. The Date Circle (Centered)
                Align(
                  alignment: Alignment.center,
                  child: Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Colors.transparent,
                      border: isPeriodDay
                          ? Border.all(
                              color: const Color(0xFFFF5252),
                              width: 1.5,
                            )
                          : (isToday
                                ? Border.all(
                                    color: const Color(0xFF9E9E9E),
                                    width: 1.5,
                                  ) // Grey for Today as per snip (looks grey/muted)
                                : null),
                    ),
                    child: Center(
                      child: Text(
                        "$day",
                        style: TextStyle(
                          color: isToday ? Colors.black : Colors.black87,
                          fontSize: 16,
                          fontWeight: isToday
                              ? FontWeight.bold
                              : FontWeight.w500,
                        ),
                      ),
                    ),
                  ),
                ),

                // 2. The Cycle Day Number (Bottom Right, Small)
                // Using Align with padding to position it cleanly away from the center circle
                if (cycleDay != null)
                  Positioned(
                    bottom: 0.2,
                    right: 0.5,
                    child: Text(
                      "$cycleDay",
                      style: TextStyle(
                        color: cycleDayColor,
                        fontSize: 8,
                        fontWeight:
                            FontWeight.w300, // Light font weight from Figma
                        height: 1.0, // Tight line height
                      ),
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildCounterRow(
    String label,
    int value,
    Function(int) onChanged,
    IconData icon,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 18, color: AppColors.primary),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey[700],
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _buildCounterButton(Icons.remove, () {
              if (value > 1) onChanged(value - 1);
            }),
            Column(
              children: [
                Text(
                  "$value",
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Text(
                  "days",
                  style: TextStyle(fontSize: 10, color: Colors.grey),
                ),
              ],
            ),
            _buildCounterButton(Icons.add, () => onChanged(value + 1)),
          ],
        ),
      ],
    );
  }

  Widget _buildCounterButton(IconData icon, VoidCallback onPressed) {
    return Container(
      width: 44,
      height: 44,
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(12),
      ),
      child: IconButton(
        icon: Icon(icon, color: Colors.black87, size: 20),
        onPressed: onPressed,
      ),
    );
  }

  Widget _buildFlowOption(String label) {
    final isSelected = _flowIntensity == label;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _flowIntensity = label),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF009688) : Colors.transparent,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: isSelected ? Colors.white : Colors.black87,
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLegendItem(Color color, String label, {required bool isFilled}) {
    return Row(
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: isFilled ? color : Colors.transparent,
            border: isFilled ? null : Border.all(color: color, width: 2),
          ),
        ),
        const SizedBox(width: 8),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey[600],
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  String _monthName(int month) {
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
    return months[month - 1];
  }
}
