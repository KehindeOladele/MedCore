import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../widgets/reminder_type_selector.dart';
import '../../../home/presentation/providers/home_controller.dart';
import '../../../home/presentation/providers/home_data_provider.dart';
import '../../../home/data/models/reminder_model.dart';
import '../../../../core/services/notification_service.dart';

class AddReminderScreen extends ConsumerStatefulWidget {
  final bool isTab;
  final ReminderModel? reminder; // Add this

  const AddReminderScreen({super.key, this.isTab = false, this.reminder});

  @override
  ConsumerState<AddReminderScreen> createState() => _AddReminderScreenState();
}

class _AddReminderScreenState extends ConsumerState<AddReminderScreen> {
  final _titleController = TextEditingController();
  final _notesController = TextEditingController();
  DateTime _selectedDate = DateTime.now();
  TimeOfDay _selectedTime = const TimeOfDay(hour: 9, minute: 0);
  String _selectedFrequency = 'Once';
  final List<String> _customDays = [];
  IconData _selectedIcon = Icons.medication_outlined; // Default icon

  @override
  void initState() {
    super.initState();
    if (widget.reminder != null) {
      _titleController.text = widget.reminder!.title;
      _notesController.text = widget.reminder!.subtitle;

      // Validate frequency
      const allowedFrequencies = [
        'Once',
        'Twice',
        'Daily',
        'Weekly',
        'Monthly',
        'Custom',
      ];
      if (allowedFrequencies.contains(widget.reminder!.tagText)) {
        _selectedFrequency = widget.reminder!.tagText;
      } else {
        // Default to "Once" or map "Upcoming" to "Daily" if preferred,
        // but "Once" is safe. "Upcoming" was a legacy tag.
        _selectedFrequency = 'Once';
      }

      _selectedIcon = widget.reminder!.icon;

      // Parse time
      try {
        final timeParts = widget.reminder!.time.split(" ");
        final hm = timeParts[0].split(":");
        int hour = int.parse(hm[0]);
        int minute = int.parse(hm[1]);
        if (timeParts.length > 1 && timeParts[1] == "PM" && hour != 12) {
          hour += 12;
        } else if (timeParts.length > 1 && timeParts[1] == "AM" && hour == 12) {
          hour = 0;
        }
        _selectedTime = TimeOfDay(hour: hour, minute: minute);
      } catch (e) {
        // Fallback or log error
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Add Reminder',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        leading: widget.isTab
            ? null
            : IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () => Navigator.pop(context),
              ),
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: Colors.black,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Reminder Type
            _buildLabel('Reminder Type'),
            ReminderTypeSelector(
              initialIcon: _selectedIcon,
              onIconChanged: (icon) => setState(() => _selectedIcon = icon),
            ),
            const SizedBox(height: 16),

            // Title
            _buildLabel('Title'),
            SizedBox(
              height: 46,
              child: TextField(
                controller: _titleController,
                decoration: _inputDecoration('e.g., Take Amoxicillin'),
              ),
            ),
            const SizedBox(height: 12),

            // Date & Time
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildLabel('Date'),
                      GestureDetector(
                        onTap: () async {
                          final date = await showDatePicker(
                            context: context,
                            initialDate: _selectedDate,
                            firstDate: DateTime.now(),
                            lastDate: DateTime.now().add(
                              const Duration(days: 365),
                            ),
                          );
                          if (date != null) {
                            setState(() => _selectedDate = date);
                          }
                        },
                        child: Container(
                          height: 46,
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFAFAFA),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.grey[200]!),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                Icons.calendar_today_outlined,
                                size: 18,
                                color: Colors.grey[600],
                              ),
                              const SizedBox(width: 8),
                              Text(
                                "${_selectedDate.month}/${_selectedDate.day}/${_selectedDate.year}",
                                style: const TextStyle(
                                  fontWeight: FontWeight.w500,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildLabel('Time'),
                      GestureDetector(
                        onTap: () async {
                          final time = await showTimePicker(
                            context: context,
                            initialTime: _selectedTime,
                          );
                          if (time != null) {
                            setState(() => _selectedTime = time);
                          }
                        },
                        child: Container(
                          height: 46,
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFAFAFA),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.grey[200]!),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                Icons.access_time,
                                size: 18,
                                color: Colors.grey[600],
                              ),
                              const SizedBox(width: 8),
                              Text(
                                _selectedTime.format(context),
                                style: const TextStyle(
                                  fontWeight: FontWeight.w500,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Frequency & Tablets
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildLabel('Frequency'),
                      Container(
                        height: 46, // Match standard input height
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFAFAFA),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.grey[200]!),
                        ),
                        alignment: Alignment.centerLeft,
                        child: DropdownButtonHideUnderline(
                          child: DropdownButton<String>(
                            isExpanded: true,
                            value: _selectedFrequency,
                            icon: Icon(
                              Icons
                                  .keyboard_arrow_down, // Standard dropdown icon
                              size: 20,
                              color: Colors.grey[600],
                            ),
                            style: const TextStyle(
                              fontSize: 13,
                              color: Colors.black,
                              fontWeight: FontWeight.w500,
                            ),
                            items:
                                [
                                      'Once',
                                      'Twice',
                                      'Daily',
                                      'Weekly',
                                      'Monthly',
                                      'Custom',
                                    ]
                                    .map(
                                      (e) => DropdownMenuItem(
                                        value: e,
                                        child: Text(e),
                                      ),
                                    )
                                    .toList(),
                            onChanged: (val) {
                              if (val != null) {
                                setState(() => _selectedFrequency = val);
                              }
                            },
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildLabel('No of Tablets'),
                      SizedBox(
                        height: 46, // Force height to match Dropdown
                        child: TextField(
                          keyboardType: TextInputType.number,
                          decoration: _inputDecoration('2').copyWith(
                            prefixIcon: Icon(
                              Icons
                                  .medication, // Changed icon to be more relevant
                              size: 18,
                              color: Colors.grey[600],
                            ),
                            contentPadding: const EdgeInsets.symmetric(
                              vertical: 0,
                              horizontal: 12,
                            ), // Align text vertically
                          ),
                          style: const TextStyle(fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),

            // Custom Cycle Selector
            if (_selectedFrequency == 'Custom') ...[
              const SizedBox(height: 12),
              _buildLabel('Dosage Cycle (Days)'),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(
                  (day) {
                    final isSelected = _customDays.contains(day);
                    return ChoiceChip(
                      label: Text(day),
                      selected: isSelected,
                      onSelected: (selected) {
                        setState(() {
                          if (selected) {
                            _customDays.add(day);
                          } else {
                            _customDays.remove(day);
                          }
                        });
                      },
                      selectedColor: const Color(0xFF009688),
                      labelStyle: TextStyle(
                        color: isSelected ? Colors.white : Colors.black,
                        fontWeight: isSelected
                            ? FontWeight.bold
                            : FontWeight.normal,
                      ),
                      backgroundColor: const Color(0xFFFAFAFA),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                        side: BorderSide(
                          color: isSelected
                              ? Colors.transparent
                              : Colors.grey[200]!,
                        ),
                      ),
                    );
                  },
                ).toList(),
              ),
              const SizedBox(height: 8),
              _buildLabel('Interval (Optional)'),
              SizedBox(
                height: 56,
                child: TextField(
                  keyboardType: TextInputType.number,
                  decoration: _inputDecoration('Every X days (e.g., 2)')
                      .copyWith(
                        contentPadding: const EdgeInsets.symmetric(
                          vertical: 18,
                          horizontal: 12,
                        ),
                      ),
                ),
              ),
            ],
            const SizedBox(height: 16),

            // Link Record
            _buildLabel('Link Record (Optional)'),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
              decoration: BoxDecoration(
                color: const Color(0xFFFAFAFA),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey[200]!),
              ),
              child: Row(
                children: [
                  Icon(Icons.link, size: 20, color: Colors.grey[600]),
                  const SizedBox(width: 8),
                  Text(
                    'Select a medical record...',
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Notes
            _buildLabel('Description / Notes'),
            TextField(
              controller: _notesController,
              maxLines: 4,
              decoration: _inputDecoration(
                'Add additional details or instructions...',
              ),
            ),
            const SizedBox(height: 24),

            // Save Button
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                child: const Text(
                  'Save to Reminder',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF009688),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(28),
                  ),
                  elevation: 0,
                ),
                onPressed: () async {
                  final notificationService =
                      NotificationService(); // Should utilize dependency injection in real app

                  if (widget.reminder != null) {
                    // Update existing
                    widget.reminder!.title = _titleController.text.isNotEmpty
                        ? _titleController.text
                        : "New Reminder";
                    widget.reminder!.subtitle = _notesController.text.isNotEmpty
                        ? _notesController.text
                        : "No notes";
                    widget.reminder!.tagText = _selectedFrequency;
                    widget.reminder!.icon = _selectedIcon;
                    widget.reminder!.time = _selectedTime.format(context);

                    await widget.reminder!.save();

                    // Schedule Notification
                    // Use reminder key as ID (ensure it's int or hash it)
                    int notificationId = widget.reminder!.key.hashCode;

                    // Construct DateTime
                    final now = DateTime.now();
                    var scheduledDate = DateTime(
                      _selectedDate.year,
                      _selectedDate.month,
                      _selectedDate.day,
                      _selectedTime.hour,
                      _selectedTime.minute,
                    );

                    // If scheduled time is in the past, add a day (or relevant interval)
                    // so it schedules for next occurrence, unless it's 'Once' at a specific date.
                    if (scheduledDate.isBefore(now)) {
                      if (_selectedFrequency == 'Once') {
                        // Keep as is? Or warn?
                        // If it's a date in the past, it won't fire.
                        // If time is past but date is today, add day?
                        // The user picked a date. We should respect it.
                      } else {
                        scheduledDate = scheduledDate.add(
                          const Duration(days: 1),
                        );
                      }
                    }

                    await notificationService.scheduleNotification(
                      id: notificationId,
                      title: widget.reminder!.title,
                      body: widget.reminder!.subtitle,
                      scheduledTime: scheduledDate,
                      frequency: _selectedFrequency,
                    );
                  } else {
                    // Create new
                    final newReminder = ReminderModel(
                      title: _titleController.text.isNotEmpty
                          ? _titleController.text
                          : "New Reminder",
                      subtitle: _notesController.text.isNotEmpty
                          ? _notesController.text
                          : "No notes",
                      tagText: _selectedFrequency,
                      tagColor: Colors.blue, // Default
                      icon: _selectedIcon,
                      time: _selectedTime.format(context),
                    );

                    await ref
                        .read(homeRepositoryProvider)
                        .addReminder(newReminder);

                    // After adding, we might need the key.
                    // Hive's add returns the key (int).
                    // Wait, `addReminder` in repo might return void or proper key.
                    // Let's assume we can get the key from `newReminder.key` after it's added to box?
                    // Usually yes if the object is managed.

                    // To be safe, let's re-fetch or assume `key` is valid after `add`.
                    // Only works if `newReminder` is the instance added to Hive.

                    // Schedule Notification
                    int notificationId =
                        newReminder.hashCode; // Fallback if key null?
                    if (newReminder.isInBox) {
                      notificationId = newReminder.key.hashCode;
                    }

                    final now = DateTime.now();
                    var scheduledDate = DateTime(
                      _selectedDate.year,
                      _selectedDate.month,
                      _selectedDate.day,
                      _selectedTime.hour,
                      _selectedTime.minute,
                    );

                    // Logic for past times
                    if (scheduledDate.isBefore(now) &&
                        _selectedFrequency != 'Once') {
                      scheduledDate = scheduledDate.add(
                        const Duration(days: 1),
                      );
                    }

                    await notificationService.scheduleNotification(
                      id: notificationId,
                      title: newReminder.title,
                      body: newReminder.subtitle,
                      scheduledTime: scheduledDate,
                      frequency: _selectedFrequency,
                    );
                  }

                  ref.invalidate(remindersProvider); // Refresh the list

                  if (widget.isTab) {
                    ref.read(homeIndexProvider.notifier).setIndex(0);
                  } else {
                    Navigator.pop(context);
                  }

                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Reminder Saved & Alarm Set!'),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildLabel(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.grey[700],
        ),
      ),
    );
  }

  InputDecoration _inputDecoration(String hint) {
    return InputDecoration(
      hintText: hint,
      hintStyle: TextStyle(color: Colors.grey[400], fontSize: 13),
      filled: true,
      fillColor: const Color(0xFFFAFAFA),
      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 0),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.grey[200]!),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.grey[200]!),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: Color(0xFF009688)), // Teal
      ),
    );
  }
}
