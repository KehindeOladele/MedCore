import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../../data/models/prescription_model.dart';
import '../../../patient_history/data/models/medical_history_model.dart';
import '../../../patient_history/data/repositories/patient_history_repository.dart';

class AddPrescriptionScreen extends StatefulWidget {
  /// When non-null, the screen is in edit mode — fields are pre-filled.
  final PrescriptionModel? prescription;

  const AddPrescriptionScreen({super.key, this.prescription});

  @override
  State<AddPrescriptionScreen> createState() => _AddPrescriptionScreenState();
}

class _AddPrescriptionScreenState extends State<AddPrescriptionScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameController;
  late final TextEditingController _dosageController;
  late final TextEditingController _doctorController;
  late final TextEditingController _instructionsController;

  late String _selectedFrequency;
  late TimeOfDay _selectedTime;
  late DateTime? _startDate;
  late DateTime? _endDate;
  late bool _setReminder;

  static const _primaryGreen = Color(0xFF059669);

  bool get _isEditing => widget.prescription != null;

  @override
  void initState() {
    super.initState();
    final p = widget.prescription;
    _nameController = TextEditingController(text: p?.name ?? '');
    _dosageController = TextEditingController(text: p?.dosage ?? '');
    _doctorController = TextEditingController(text: p?.doctor ?? '');
    _instructionsController = TextEditingController(
      text: p?.instructions ?? '',
    );
    _selectedFrequency = p?.frequency ?? 'Once';
    _selectedTime = p?.reminderTime ?? const TimeOfDay(hour: 8, minute: 0);
    _startDate = p?.startDate;
    _endDate = p?.endDate;
    _setReminder = p?.hasReminder ?? true;
  }

  @override
  void dispose() {
    _nameController.dispose();
    _dosageController.dispose();
    _doctorController.dispose();
    _instructionsController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(bool isStart) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now().subtract(const Duration(days: 365)),
      lastDate: DateTime(2030),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(
              primary: _primaryGreen,
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
        if (isStart)
          _startDate = picked;
        else
          _endDate = picked;
      });
    }
  }

  void _save() {
    if (!_formKey.currentState!.validate()) return;

    final store = PrescriptionStore.instance;

    if (_isEditing) {
      store.update(
        widget.prescription!.copyWith(
          name: _nameController.text,
          dosage: _dosageController.text,
          frequency: _selectedFrequency,
          doctor: _doctorController.text,
          instructions: _instructionsController.text,
          startDate: _startDate,
          endDate: _endDate,
          reminderTime: _selectedTime,
          hasReminder: _setReminder,
        ),
      );
    } else {
      final prescription = PrescriptionModel(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        name: _nameController.text,
        dosage: _dosageController.text.isNotEmpty
            ? _dosageController.text
            : 'As directed',
        frequency: _selectedFrequency,
        doctor: _doctorController.text,
        instructions: _instructionsController.text,
        startDate: _startDate,
        endDate: _endDate,
        reminderTime: _selectedTime,
        hasReminder: _setReminder,
      );
      store.add(prescription);

      // ADD TO MEDICAL HISTORY
      PatientHistoryRepository.instance.addItem(
        MedicalHistoryItem(
          date: DateTime.now(),
          title: "Igwe Pharmacy", // Default pharmacy for new prescriptions
          subtitle:
              "Refill #${prescription.id.substring(prescription.id.length - 5)}",
          description: "${prescription.name} ${prescription.dosage}",
          actionText: "VIEW PRESCRIPTION",
          type: "pharmacy",
        ),
      );
    }

    context.pop();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          _isEditing ? 'Prescription Updated!' : 'Prescription Saved!',
        ),
        backgroundColor: _primaryGreen,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text(
          _isEditing ? 'Edit Prescription' : 'Add Prescriptions',
          style: const TextStyle(
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
          onPressed: () => context.pop(),
        ),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(20.w),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Prescriptions',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 16.h),

              _buildSectionLabel('MEDICATION DETAILS'),
              SizedBox(height: 8.h),
              _buildTextField(
                controller: _nameController,
                hint: 'Name e.g., Amoxicillin',
              ),
              SizedBox(height: 16.h),

              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSectionLabel('DOSAGE'),
                        SizedBox(height: 8.h),
                        _buildTextField(
                          controller: _dosageController,
                          hint: '500mg',
                        ),
                      ],
                    ),
                  ),
                  SizedBox(width: 16.w),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSectionLabel('FREQUENCY'),
                        SizedBox(height: 8.h),
                        Container(
                          height: 48.h,
                          padding: EdgeInsets.symmetric(horizontal: 12.w),
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
                                if (val != null)
                                  setState(() => _selectedFrequency = val);
                              },
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16.h),

              _buildSectionLabel('DURATION'),
              SizedBox(height: 8.h),
              Row(
                children: [
                  Expanded(
                    child: _buildDatePickerField(
                      label: 'START',
                      date: _startDate,
                      onTap: () => _selectDate(true),
                    ),
                  ),
                  SizedBox(width: 16.w),
                  Expanded(
                    child: _buildDatePickerField(
                      label: 'STOP',
                      date: _endDate,
                      onTap: () => _selectDate(false),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16.h),

              _buildSectionLabel('PRESCRIBING DOCTOR'),
              SizedBox(height: 8.h),
              _buildTextField(
                controller: _doctorController,
                hint: 'DR. Israel',
              ),
              SizedBox(height: 16.h),

              _buildSectionLabel('INSTRUCTIONS'),
              SizedBox(height: 8.h),
              _buildTextField(
                controller: _instructionsController,
                hint: 'Take after a meal with a full glass of water',
                maxLines: 3,
              ),
              SizedBox(height: 16.h),

              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Set a Reminder',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  Switch(
                    value: _setReminder,
                    activeColor: _primaryGreen,
                    activeTrackColor: _primaryGreen.withValues(alpha: 0.2),
                    onChanged: (v) => setState(() => _setReminder = v),
                  ),
                ],
              ),

              if (_setReminder) ...[
                SizedBox(height: 16.h),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Reminder Time',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    InkWell(
                      onTap: () async {
                        final picked = await showTimePicker(
                          context: context,
                          initialTime: _selectedTime,
                        );
                        if (picked != null)
                          setState(() => _selectedTime = picked);
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
                                color: _primaryGreen,
                              ),
                            ),
                            const SizedBox(width: 8),
                            const Icon(
                              Icons.access_time,
                              size: 16,
                              color: _primaryGreen,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ],

              SizedBox(height: 24.h),

              SizedBox(
                width: double.infinity,
                height: 56.h,
                child: ElevatedButton(
                  onPressed: _save,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _primaryGreen,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                    elevation: 0,
                  ),
                  child: Text(
                    _isEditing ? 'Update Prescription' : 'Save Prescription',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              SizedBox(height: 20.h),
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
          borderSide: const BorderSide(color: _primaryGreen),
        ),
      ),
      validator: (v) =>
          (v == null || v.isEmpty) ? 'Please enter a value' : null,
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
                      ? '${date.month.toString().padLeft(2, '0')}/${date.day.toString().padLeft(2, '0')}/${date.year}'
                      : 'MM/DD/YYYY',
                  style: TextStyle(
                    color: date != null ? Colors.black : Colors.grey[400],
                    fontWeight: FontWeight.w500,
                    fontSize: 13,
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
