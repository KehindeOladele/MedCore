import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class VitalsCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color iconColor;
  final Color iconBackgroundColor;
  final Color backgroundColor;
  final bool showChevron;
  final VoidCallback? onTap;

  const VitalsCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.iconColor,
    required this.iconBackgroundColor,
    this.backgroundColor = AppColors.surface,
    this.showChevron = false,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: backgroundColor,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.grey.withOpacity(0.1)),
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
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: iconBackgroundColor,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(icon, color: iconColor, size: 20),
                ),
                if (showChevron)
                  const Icon(Icons.chevron_right, color: Colors.grey, size: 20),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: title == "Penicillin"
                        ? AppColors.redAccent
                        : AppColors.textPrimary, // Special case for allergy
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
