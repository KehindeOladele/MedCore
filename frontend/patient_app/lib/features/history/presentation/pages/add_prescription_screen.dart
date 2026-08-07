import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../home/presentation/providers/home_data_provider.dart';
import '../../../home/data/models/prescription_model.dart';
import '../../../home/data/models/reminder_model.dart';
import '../../../../core/services/notification_service.dart';

class AddPrescriptionScreen extends ConsumerStatefulWidget {
  final PrescriptionModel? prescription;
  const AddPrescriptionScreen({super.key, this.prescription});

  @override
  ConsumerState<AddPrescriptionScreen> createState() =>
      _AddPrescriptionScreenState();
}

class _AddPrescriptionScreenState extends ConsumerState<AddPrescriptionScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _dosageController;
  // late TextEditingController _frequencyController; // Removed
  late TextEditingController _doctorController;
  late TextEditingController _instructionsController;

  String _selectedFrequency = 'Once'; // Added
  TimeOfDay _selectedTime = const TimeOfDay(
    hour: 8,
    minute: 0,
  ); // Added for Reminder

  DateTime? _startDate;
  DateTime? _endDate;
  bool _setReminder = true;

  @override
  void initState() {
    super.initState();
    final p = widget.prescription;
    _nameController = TextEditingController(text: p?.title ?? '');
    _dosageController = TextEditingController(text: p?.dosage ?? '');
    // _frequencyController removed
    _doctorController = TextEditingController();
    _instructionsController = TextEditingController(text: p?.schedule ?? '');

    if (p != null) {
      const allowedFrequencies = [
        'Once',
        'Twice',
        'Daily',
        'Weekly',
        'Monthly',
        'Custom',
      ];
      if (allowedFrequencies.contains(p.subtitle)) {
        _selectedFrequency = p.subtitle;
      }
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _dosageController.dispose();
    // _frequencyController.dispose(); // Removed
    _doctorController.dispose();
    _instructionsController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context, bool isStart) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2030),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(
              primary: AppColors.primary,
              onPrimary: Colors.white,
              onSurface: Colors.black,
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() {
        if (isStart) {
          _startDate = picked;
        } else {
          _endDate = picked;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          "Add Prescriptions",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        actions: const [],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Prescriptions",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),

              // Medication Name
              _buildSectionLabel("MEDICATION DETAILS"),
              const SizedBox(height: 8),
              _buildTextField(
                controller: _nameController,
                hint: "Name e.g., Amoxicillin",
              ),
              const SizedBox(height: 16),

              // Dosage & Frequency
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSectionLabel("DOSAGE"),
                        const SizedBox(height: 8),
                        _buildTextField(
                          controller: _dosageController,
                          hint: "500mg",
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSectionLabel("FREQUENCY"),
                        const SizedBox(height: 8),
                        Container(
                          height: 48, // Standard input height
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
                                Icons.keyboard_arrow_down,
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
                ],
              ),
              const SizedBox(height: 16),

              // Duration
              _buildSectionLabel("DURATION"),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: _buildDatePickerField(
                      label: "START",
                      date: _startDate,
                      onTap: () => _selectDate(context, true),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: _buildDatePickerField(
                      label: "STOP",
                      date: _endDate,
                      onTap: () => _selectDate(context, false),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Prescribing Doctor
              _buildSectionLabel("PRESCRIBING DOCTOR"),
              const SizedBox(height: 8),
              _buildTextField(
                controller: _doctorController,
                hint: "DR. Israel",
              ),
              const SizedBox(height: 16),

              // Instructions
              _buildSectionLabel("INSTRUCTIONS"),
              const SizedBox(height: 8),
              _buildTextField(
                controller: _instructionsController,
                hint: "Take after a meal with a full glass of water",
                maxLines: 3,
              ),
              const SizedBox(height: 16),

              // Reminder Toggle
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    "Set a Reminder",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  Switch(
                    value: _setReminder,
                    activeColor: AppColors.primary,
                    activeTrackColor: AppColors.primary.withOpacity(0.2),
                    onChanged: (value) {
                      setState(() {
                        _setReminder = value;
                      });
                    },
                  ),
                ],
              ),
              if (_setReminder) ...[
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Reminder Time",
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    InkWell(
                      onTap: () async {
                        final TimeOfDay? picked = await showTimePicker(
                          context: context,
                          initialTime: _selectedTime,
                        );
                        if (picked != null) {
                          setState(() {
                            _selectedTime = picked;
                          });
                        }
                      },
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFAFAFA),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.grey[300]!),
                        ),
                        child: Row(
                          children: [
                            Text(
                              _selectedTime.format(context),
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                color: AppColors.primary,
                              ),
                            ),
                            const SizedBox(width: 8),
                            const Icon(
                              Icons.access_time,
                              size: 16,
                              color: AppColors.primary,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ],
              const SizedBox(height: 24),

              // Save Button
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: () async {
                    if (_formKey.currentState!.validate()) {
                      // 1. Save Prescription
                      final newPrescription = PrescriptionModel(
                        id:
                            widget.prescription?.id ??
                            DateTime.now().millisecondsSinceEpoch.toString(),
                        title: _nameController.text,
                        subtitle: _selectedFrequency,
                        dosage: _dosageController.text.isNotEmpty
                            ? _dosageController.text
                            : "As directed",
                        schedule: _instructionsController.text.isNotEmpty
                            ? _instructionsController.text
                            : "See instructions",
                        icon: Icons.medication,
                        iconColor: const Color(0xFF009688),
                        iconBackgroundColor: const Color(0xFFE0F2F1),
                        badgeColor: const Color(0xFFF5F5F5),
                        backgroundColor: const Color(0xFFF0FDFA),
                      );

                      await ref
                          .read(homeRepositoryProvider)
                          .addPrescription(newPrescription);
                      ref.invalidate(prescriptionsProvider);

                      // 2. Set Reminder if enabled
                      if (_setReminder) {
                        try {
                          final notificationService = NotificationService();
                          final reminderTime = _selectedTime.format(context);

                          final newReminder = ReminderModel(
                            title: "Take ${_nameController.text}",
                            subtitle: _dosageController.text,
                            time: reminderTime,
                            tagText: _selectedFrequency,
                            tagColor: AppColors.primary,
                            icon: Icons.medication,
                          );

                          await ref
                              .read(homeRepositoryProvider)
                              .addReminder(newReminder);
                          ref.invalidate(remindersProvider);

                          // Schedule Notification
                          // Generate a unique ID for the notification
                          final notificationId =
                              DateTime.now().millisecondsSinceEpoch ~/ 1000;

                          final now = DateTime.now();
                          var scheduledDate = DateTime(
                            now.year,
                            now.month,
                            now.day,
                            _selectedTime.hour,
                            _selectedTime.minute,
                          );

                          // If time is in past, schedule for tomorrow (unless it's 'Once' at specific date, but here we assume daily flow)
                          // For simplicity, if past, add 1 day if not 'Once' or just let it trigger immediately/fail?
                          // Let's stick to standard behavior: if past, add a day.
                          if (scheduledDate.isBefore(now)) {
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
                        } catch (e) {
                          debugPrint("Error setting reminder: $e");
                        }
                      }

                      if (context.mounted) {
                        Navigator.pop(context);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                              _setReminder
                                  ? 'Prescription & Reminder Saved!'
                                  : 'Prescription Saved!',
                            ),
                          ),
                        );
                      }
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                    elevation: 0,
                  ),
                  child: const Text(
                    "Save Prescription",
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionLabel(String label) {
    return Text(
      label,
      style: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.bold,
        color: Colors.grey[600],
        letterSpacing: 0.5,
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hint,
    int maxLines = 1,
  }) {
    return TextFormField(
      controller: controller,
      maxLines: maxLines,
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: TextStyle(color: Colors.grey[400]),
        filled: true,
        fillColor: const Color(0xFFFAFAFA),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 12,
          vertical: 12,
        ),
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
          borderSide: const BorderSide(color: AppColors.primary),
        ),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter a value';
        }
        return null;
      },
    );
  }

  Widget _buildDatePickerField({
    required String label,
    DateTime? date,
    required VoidCallback onTap,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.bold,
            color: Colors.grey[500],
          ),
        ),
        const SizedBox(height: 4),
        GestureDetector(
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(
              color: const Color(0xFFFAFAFA),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.grey[200]!),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  date != null
                      ? "${date.month.toString().padLeft(2, '0')}/${date.day.toString().padLeft(2, '0')}/${date.year}"
                      : "MM/DD/YYYY",
                  style: TextStyle(
                    color: date != null ? Colors.black : Colors.grey[400],
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Icon(
                  Icons.calendar_today_outlined,
                  size: 18,
                  color: Colors.grey[400],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
