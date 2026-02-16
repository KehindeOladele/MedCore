import 'package:flutter/material.dart';
import '../../data/models/allergy_model.dart';

class AddAllergyForm extends StatefulWidget {
  final Function(String name, String reaction, AllergySeverity severity)?
  onSubmit;

  const AddAllergyForm({super.key, this.onSubmit});

  @override
  State<AddAllergyForm> createState() => _AddAllergyFormState();
}

class _AddAllergyFormState extends State<AddAllergyForm> {
  final _allergenNameController = TextEditingController();
  final _reactionController = TextEditingController();
  AllergySeverity? _selectedSeverity;

  @override
  void dispose() {
    _allergenNameController.dispose();
    _reactionController.dispose();
    super.dispose();
  }

  void _handleSubmit() {
    if (_allergenNameController.text.isEmpty ||
        _reactionController.text.isEmpty ||
        _selectedSeverity == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in all fields')),
      );
      return;
    }

    widget.onSubmit?.call(
      _allergenNameController.text,
      _reactionController.text,
      _selectedSeverity!,
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Allergen Name
          Text(
            'Allergen Name',
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
              color: const Color(0xFF374151),
            ),
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _allergenNameController,
            decoration: InputDecoration(
              hintText: 'Enter Allergen name',
              hintStyle: const TextStyle(color: Color(0xFF9ca3af)),
              filled: true,
              fillColor: const Color(0xFFf9fafb),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFe5e7eb)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFe5e7eb)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(
                  color: Color(0xFF3b82f6),
                  width: 2,
                ),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 13,
              ),
            ),
          ),
          const SizedBox(height: 28),

          // Reaction
          Text(
            'Reaction',
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
              color: const Color(0xFF374151),
            ),
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _reactionController,
            minLines: 5,
            maxLines: 8,
            decoration: InputDecoration(
              hintText:
                  'Describe the reaction (e.g hives, swelling, difficulty breathing)',
              hintStyle: const TextStyle(color: Color(0xFF9ca3af)),
              filled: true,
              fillColor: const Color(0xFFf9fafb),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFe5e7eb)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFe5e7eb)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(
                  color: Color(0xFF3b82f6),
                  width: 2,
                ),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 12,
              ),
            ),
          ),
          const SizedBox(height: 28),

          // Severity Level
          Text(
            'Severity Level',
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
              color: const Color(0xFF374151),
            ),
          ),
          const SizedBox(height: 12),

          // Severity Buttons - Row 1
          Row(
            children: [
              Expanded(
                child: _SeverityButton(
                  label: 'Mild',
                  severity: AllergySeverity.mild,
                  isSelected: _selectedSeverity == AllergySeverity.mild,
                  backgroundColor: const Color(0xFFdbeafe),
                  borderColor: const Color(0xFFbfdbfe),
                  textColor: const Color(0xFF1d4ed8),
                  dotColor: const Color(0xFF3b82f6),
                  onPressed: () {
                    setState(() {
                      _selectedSeverity = AllergySeverity.mild;
                    });
                  },
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _SeverityButton(
                  label: 'Moderate',
                  severity: AllergySeverity.moderate,
                  isSelected: _selectedSeverity == AllergySeverity.moderate,
                  backgroundColor: const Color(0xFFfef9c3),
                  borderColor: const Color(0xFFfef08a),
                  textColor: const Color(0xFFa16207),
                  dotColor: const Color(0xFFeab308),
                  onPressed: () {
                    setState(() {
                      _selectedSeverity = AllergySeverity.moderate;
                    });
                  },
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Severity Buttons - Row 2
          Row(
            children: [
              Expanded(
                child: _SeverityButton(
                  label: 'Severe',
                  severity: AllergySeverity.severe,
                  isSelected: _selectedSeverity == AllergySeverity.severe,
                  backgroundColor: const Color(0xFFffedd5),
                  borderColor: const Color(0xFFfed7aa),
                  textColor: const Color(0xFFc2410c),
                  dotColor: const Color(0xFFf97316),
                  onPressed: () {
                    setState(() {
                      _selectedSeverity = AllergySeverity.severe;
                    });
                  },
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _SeverityButton(
                  label: 'Anaphylactic',
                  severity: AllergySeverity.anaphylactic,
                  isSelected: _selectedSeverity == AllergySeverity.anaphylactic,
                  backgroundColor: const Color(0xFFfee2e2),
                  borderColor: const Color(0xFFfecaca),
                  textColor: const Color(0xFFb91c1c),
                  dotColor: const Color(0xFFef4444),
                  onPressed: () {
                    setState(() {
                      _selectedSeverity = AllergySeverity.anaphylactic;
                    });
                  },
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),

          // Submit Button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _handleSubmit,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00C853),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: const Text(
                'Add Allergen',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}

class _SeverityButton extends StatelessWidget {
  final String label;
  final AllergySeverity severity;
  final bool isSelected;
  final Color backgroundColor;
  final Color borderColor;
  final Color textColor;
  final Color dotColor;
  final VoidCallback onPressed;

  const _SeverityButton({
    required this.label,
    required this.severity,
    required this.isSelected,
    required this.backgroundColor,
    required this.borderColor,
    required this.textColor,
    required this.dotColor,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        height: 50,
        decoration: BoxDecoration(
          color: backgroundColor,
          border: Border.all(color: borderColor, width: 1.5),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Stack(
          children: [
            // Dot indicator
            Positioned(
              left: 12,
              top: 50 / 2 - 6,
              child: Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(
                  color: dotColor,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 2),
                ),
              ),
            ),
            // Text
            Align(
              alignment: Alignment.center,
              child: Text(
                label,
                style: TextStyle(
                  color: textColor,
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
