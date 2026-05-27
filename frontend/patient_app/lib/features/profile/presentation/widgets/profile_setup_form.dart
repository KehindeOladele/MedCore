import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../../data/models/profile_model.dart';
import '../providers/profile_provider.dart';
import '../../../home/presentation/providers/home_data_provider.dart';

class ProfileSetupForm extends ConsumerStatefulWidget {
  final ProfileModel profile;
  const ProfileSetupForm({super.key, required this.profile});

  @override
  ConsumerState<ProfileSetupForm> createState() => _ProfileSetupFormState();
}

class _ProfileSetupFormState extends ConsumerState<ProfileSetupForm> {
  final _formKey = GlobalKey<FormState>();
  
  late final TextEditingController _firstNameController;
  late final TextEditingController _lastNameController;
  late final TextEditingController _heightController;
  late final TextEditingController _weightController;
  late final TextEditingController _allergyInputController;
  
  DateTime? _selectedDate;
  String? _selectedGender;
  String? _selectedBloodGroup;
  String? _selectedGenotype;
  
  final List<String> _allergies = [];
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _firstNameController = TextEditingController(text: widget.profile.firstName);
    _lastNameController = TextEditingController(text: widget.profile.lastName);
    _heightController = TextEditingController(
      text: widget.profile.height != null ? widget.profile.height!.toStringAsFixed(0) : '',
    );
    _weightController = TextEditingController(
      text: widget.profile.weight != null ? widget.profile.weight!.toStringAsFixed(0) : '',
    );
    _allergyInputController = TextEditingController();
    
    _selectedDate = widget.profile.dateOfBirth;
    _selectedGender = widget.profile.gender;
    _selectedBloodGroup = widget.profile.bloodGroup;
    
    // Prefill genotype and allergies if already present in fhir_metadata
    _selectedGenotype = widget.profile.genotype;
    _allergies.addAll(widget.profile.allergies);
  }

  @override
  void dispose() {
    _firstNameController.dispose();
    _lastNameController.dispose();
    _heightController.dispose();
    _weightController.dispose();
    _allergyInputController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate ?? DateTime(2000, 1, 1),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(
              primary: AppColors.primary,
              onPrimary: Colors.white,
              onSurface: AppColors.textPrimary,
            ),
          ),
          child: child!,
        );
      },
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  void _addAllergy() {
    final allergy = _allergyInputController.text.trim();
    if (allergy.isNotEmpty && !_allergies.contains(allergy)) {
      setState(() {
        _allergies.add(allergy);
        _allergyInputController.clear();
      });
    }
  }

  void _removeAllergy(String allergy) {
    setState(() {
      _allergies.remove(allergy);
    });
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your Date of Birth')),
      );
      return;
    }
    if (_selectedGender == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your Gender')),
      );
      return;
    }
    if (_selectedBloodGroup == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your Blood Group')),
      );
      return;
    }
    if (_selectedGenotype == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your Genotype')),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final double height = double.parse(_heightController.text.trim());
      final double weight = double.parse(_weightController.text.trim());

      final payload = {
        'first_name': _firstNameController.text.trim(),
        'last_name': _lastNameController.text.trim(),
        'gender': _selectedGender,
        'blood_group': _selectedBloodGroup,
        'date_of_birth': _selectedDate!.toIso8601String().split('T').first,
        'fhir_metadata': {
          'resourceType': 'Patient',
          'height': height,
          'weight': weight,
          'genotype': _selectedGenotype,
          'allergies': _allergies,
        }
      };

      // Call profile update provider
      await ref.read(profileProvider.notifier).updateProfile(payload);
      
      // Invalidate dashboard and summary providers to reload widgets
      ref.invalidate(userSummaryProvider);
      ref.invalidate(vitalsProvider);
      ref.invalidate(profileProvider);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile setup completed successfully!'),
            backgroundColor: AppColors.primary,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to update profile: $e'),
            backgroundColor: AppColors.redAccent,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Complete Your Profile",
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.textPrimary,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              "Fill in your personal and primary clinical information to set up your account and vitals board.",
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
                height: 1.4,
              ),
            ),
            const SizedBox(height: 32),

            // --- SECTION: Personal Info ---
            _buildSectionHeader("Personal Details"),
            const SizedBox(height: 16),
            
            _buildTextField(
              controller: _firstNameController,
              label: "First Name",
              hintText: "e.g., Kehinde",
              validator: (value) =>
                  value == null || value.trim().isEmpty ? "First name is required" : null,
            ),
            const SizedBox(height: 16),
            
            _buildTextField(
              controller: _lastNameController,
              label: "Last Name",
              hintText: "e.g., Oladele",
              validator: (value) =>
                  value == null || value.trim().isEmpty ? "Last name is required" : null,
            ),
            const SizedBox(height: 16),

            // Date of Birth Field
            const Text(
              "Date of Birth",
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            InkWell(
              onTap: () => _selectDate(context),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                decoration: BoxDecoration(
                  color: const Color(0xFFFAFAFA),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey[200]!),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      _selectedDate == null
                          ? "Select Date"
                          : DateFormat('dd MMM, yyyy').format(_selectedDate!),
                      style: TextStyle(
                        fontSize: 16,
                        color: _selectedDate == null ? Colors.grey[400] : AppColors.textPrimary,
                      ),
                    ),
                    const Icon(Icons.calendar_today, color: AppColors.primary, size: 20),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Gender Field
            _buildDropdownField<String>(
              label: "Gender",
              value: _selectedGender,
              items: const [
                DropdownMenuItem(value: "female", child: Text("Female")),
                DropdownMenuItem(value: "male", child: Text("Male")),
              ],
              onChanged: (val) => setState(() => _selectedGender = val),
            ),
            const SizedBox(height: 32),

            // --- SECTION: Medical Vitals ---
            _buildSectionHeader("Medical Vitals"),
            const SizedBox(height: 16),

            // Blood Group Field
            _buildDropdownField<String>(
              label: "Blood Group",
              value: _selectedBloodGroup,
              items: const [
                DropdownMenuItem(value: "A+", child: Text("A+")),
                DropdownMenuItem(value: "A-", child: Text("A-")),
                DropdownMenuItem(value: "B+", child: Text("B+")),
                DropdownMenuItem(value: "B-", child: Text("B-")),
                DropdownMenuItem(value: "AB+", child: Text("AB+")),
                DropdownMenuItem(value: "AB-", child: Text("AB-")),
                DropdownMenuItem(value: "O+", child: Text("O+")),
                DropdownMenuItem(value: "O-", child: Text("O-")),
              ],
              onChanged: (val) => setState(() => _selectedBloodGroup = val),
            ),
            const SizedBox(height: 16),

            // Genotype Field
            _buildDropdownField<String>(
              label: "Genotype",
              value: _selectedGenotype,
              items: const [
                DropdownMenuItem(value: "AA", child: Text("AA")),
                DropdownMenuItem(value: "AS", child: Text("AS")),
                DropdownMenuItem(value: "SS", child: Text("SS")),
                DropdownMenuItem(value: "AC", child: Text("AC")),
              ],
              onChanged: (val) => setState(() => _selectedGenotype = val),
            ),
            const SizedBox(height: 16),

            // Height (cm) Field
            _buildTextField(
              controller: _heightController,
              label: "Height (cm)",
              hintText: "e.g., 175",
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.trim().isEmpty) return "Height is required";
                final height = double.tryParse(value);
                if (height == null || height < 30 || height > 280) {
                  return "Please enter a valid height (30-280 cm)";
                }
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Weight (kg) Field
            _buildTextField(
              controller: _weightController,
              label: "Weight (kg)",
              hintText: "e.g., 72",
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.trim().isEmpty) return "Weight is required";
                final weight = double.tryParse(value);
                if (weight == null || weight < 2 || weight > 500) {
                  return "Please enter a valid weight (2-500 kg)";
                }
                return null;
              },
            ),
            const SizedBox(height: 32),

            // --- SECTION: Allergies ---
            _buildSectionHeader("Allergies"),
            const SizedBox(height: 8),
            Text(
              "Add any known drug, food, or environmental allergies.",
              style: TextStyle(fontSize: 13, color: Colors.grey[600]),
            ),
            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: _buildTextField(
                    controller: _allergyInputController,
                    label: "",
                    hintText: "e.g., Penicillin, Peanuts",
                    onFieldSubmitted: (_) => _addAllergy(),
                  ),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: _addAllergy,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryVariant,
                    foregroundColor: AppColors.primary,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Icon(Icons.add),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (_allergies.isNotEmpty) ...[
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: _allergies.map((allergy) {
                  return Chip(
                    label: Text(allergy),
                    backgroundColor: AppColors.redBackground,
                    labelStyle: const TextStyle(
                      color: AppColors.redAccent,
                      fontWeight: FontWeight.w600,
                    ),
                    deleteIcon: const Icon(Icons.close, size: 16, color: AppColors.redAccent),
                    onDeleted: () => _removeAllergy(allergy),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                      side: BorderSide(color: AppColors.redAccent.withOpacity(0.1)),
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 16),
            ],

            const SizedBox(height: 48),

            // Save / Submit Button
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: _isSubmitting ? null : _submitForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  disabledBackgroundColor: AppColors.primary.withOpacity(0.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(26),
                  ),
                  elevation: 0,
                ),
                child: _isSubmitting
                    ? const SizedBox(
                        height: 24,
                        width: 24,
                        child: CircularProgressIndicator(
                          strokeWidth: 2.5,
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      )
                    : const Text(
                        "Save and Continue",
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 4),
        Container(
          width: 40,
          height: 3,
          decoration: BoxDecoration(
            color: AppColors.primary,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
      ],
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required String hintText,
    TextInputType keyboardType = TextInputType.text,
    String? Function(String?)? validator,
    void Function(String)? onFieldSubmitted,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (label.isNotEmpty) ...[
          Text(
            label,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 8),
        ],
        TextFormField(
          controller: controller,
          keyboardType: keyboardType,
          validator: validator,
          onFieldSubmitted: onFieldSubmitted,
          decoration: InputDecoration(
            hintText: hintText,
            hintStyle: TextStyle(color: Colors.grey[400]),
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
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
              borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.redAccent, width: 1.0),
            ),
            focusedErrorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.redAccent, width: 1.5),
            ),
            filled: true,
            fillColor: const Color(0xFFFAFAFA),
          ),
        ),
      ],
    );
  }

  Widget _buildDropdownField<T>({
    required String label,
    required T? value,
    required List<DropdownMenuItem<T>> items,
    required void Function(T?) onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<T>(
          value: value,
          items: items,
          onChanged: onChanged,
          validator: (val) => val == null ? "Please select a value" : null,
          decoration: InputDecoration(
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
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
              borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
            ),
            filled: true,
            fillColor: const Color(0xFFFAFAFA),
          ),
        ),
      ],
    );
  }
}
