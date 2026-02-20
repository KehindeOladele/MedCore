import 'package:flutter/material.dart';

import '../../data/models/allergy_model.dart';

class AllergyItem extends StatelessWidget {
  final AllergyModel allergy;

  const AllergyItem({super.key, required this.allergy});

  Color _getSeverityColor(AllergySeverity severity) {
    switch (severity) {
      case AllergySeverity.anaphylactic:
        return const Color(0xFFFF5252); // Red
      case AllergySeverity.severe:
        return const Color(0xFFFF9800); // Orange
      case AllergySeverity.moderate:
        return const Color(0xFFFFC107); // Amber/Yellow
      case AllergySeverity.mild:
        return const Color(0xFF2196F3); // Blue
    }
  }

  Color _getBadgeBackgroundColor(AllergySeverity severity) {
    switch (severity) {
      case AllergySeverity.anaphylactic:
        return const Color(0xFFFFEBEE);
      case AllergySeverity.severe:
        return const Color(0xFFFFF3E0);
      case AllergySeverity.moderate:
        return const Color(0xFFFFF8E1);
      case AllergySeverity.mild:
        return const Color(0xFFE3F2FD);
    }
  }

  String _getSeverityLabel(AllergySeverity severity) {
    switch (severity) {
      case AllergySeverity.anaphylactic:
        return 'Anaphylactic';
      case AllergySeverity.severe:
        return 'Severe';
      case AllergySeverity.moderate:
        return 'Moderate';
      case AllergySeverity.mild:
        return 'Mild';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            offset: const Offset(0, 4),
            blurRadius: 16,
          ),
        ],
      ),
      child: IntrinsicHeight(
        child: Row(
          children: [
            // Left border strip for Critical/Anaphylactic/Severe logic if needed
            // The design shows a red strip for Peanuts and orange for Penicillin.
            if (allergy.isCritical)
              Container(
                width: 6,
                decoration: BoxDecoration(
                  color: _getSeverityColor(allergy.severity),
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(16),
                    bottomLeft: Radius.circular(16),
                  ),
                ),
              ),

            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Icon Box
                    Container(
                      width: 48,
                      height: 48,
                      decoration: BoxDecoration(
                        color: _getSeverityColor(
                          allergy.severity,
                        ).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Icon(
                        allergy.icon ?? Icons.warning,
                        color: _getSeverityColor(allergy.severity),
                      ),
                    ),
                    const SizedBox(width: 16),

                    // Content
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                allergy.name,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black87,
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 8,
                                  vertical: 4,
                                ),
                                decoration: BoxDecoration(
                                  color: _getBadgeBackgroundColor(
                                    allergy.severity,
                                  ),
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(
                                    color: _getSeverityColor(allergy.severity),
                                    width: 1,
                                  ),
                                ),
                                child: Text(
                                  _getSeverityLabel(allergy.severity),
                                  style: TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.bold,
                                    color: _getSeverityColor(allergy.severity),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(
                            allergy.symptoms,
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey[600],
                              height: 1.4,
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(width: 8),
                    // Edit Icon
                    Icon(
                      Icons.edit_outlined,
                      size: 20,
                      color: Colors.grey[400],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
