import 'package:flutter/material.dart';

class ReminderTypeSelector extends StatefulWidget {
  final IconData? initialIcon;
  final Function(IconData) onIconChanged;

  const ReminderTypeSelector({
    super.key,
    this.initialIcon,
    required this.onIconChanged,
  });

  @override
  State<ReminderTypeSelector> createState() => _ReminderTypeSelectorState();
}

class _ReminderTypeSelectorState extends State<ReminderTypeSelector> {
  late int _selectedIndex;

  final List<Map<String, dynamic>> _types = [
    {'label': 'Meds', 'icon': Icons.medication_outlined},
    {'label': 'Check Ups', 'icon': Icons.calendar_today_outlined},
    {'label': 'Test', 'icon': Icons.health_and_safety_outlined},
    {'label': 'Other', 'icon': Icons.note_alt_outlined},
  ];

  @override
  void initState() {
    super.initState();
    _selectedIndex = 0;
    if (widget.initialIcon != null) {
      final index = _types.indexWhere((t) => t['icon'] == widget.initialIcon);
      if (index != -1) {
        _selectedIndex = index;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: List.generate(_types.length, (index) {
        final isSelected = _selectedIndex == index;
        return Expanded(
          child: GestureDetector(
            onTap: () {
              setState(() => _selectedIndex = index);
              widget.onIconChanged(_types[index]['icon'] as IconData);
            },
            child: Container(
              margin: EdgeInsets.only(
                right: index == _types.length - 1 ? 0 : 8,
              ),
              padding: const EdgeInsets.symmetric(vertical: 16),
              decoration: BoxDecoration(
                color: isSelected ? const Color(0xFFE0F2F1) : Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: isSelected
                      ? const Color(0xFF009688)
                      : Colors.grey[200]!,
                  width: 1.5,
                ),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    _types[index]['icon'] as IconData,
                    color: isSelected ? const Color(0xFF009688) : Colors.black,
                    size: 24,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _types[index]['label'] as String,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: isSelected
                          ? const Color(0xFF009688)
                          : Colors.black,
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      }),
    );
  }
}
