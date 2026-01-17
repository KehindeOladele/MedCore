import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../data/models/prescription_model.dart';

class PrescriptionCard extends StatelessWidget {
  final PrescriptionModel prescription;

  const PrescriptionCard({super.key, required this.prescription});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: prescription.backgroundColor ?? AppColors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.grey.withOpacity(0.2)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: prescription.iconBackgroundColor,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(
                  prescription.icon,
                  color: prescription.iconColor,
                  size: 24,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      prescription.title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: const Color(0xFF1A1C1E),
                      ),
                    ),
                    Text(
                      prescription.subtitle,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: prescription.badgeColor ?? const Color(0xFFF5F5F5),
                  borderRadius: BorderRadius.circular(20), // Pill shape
                  border: Border.all(
                    color: Colors.grey.withOpacity(
                      0.2,
                    ), // The "Ribbon" (Border)
                    width: 1,
                  ),
                ),
                child: Text(
                  prescription.dosage,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.black87,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Icon(
                Icons.access_time_rounded,
                size: 16,
                color: Colors.grey[400],
              ),
              const SizedBox(width: 8),
              Text(
                prescription.schedule,
                style: Theme.of(
                  context,
                ).textTheme.bodySmall?.copyWith(color: Colors.grey[600]),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
