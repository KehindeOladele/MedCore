import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../home/presentation/widgets/vitals_card.dart';

class ProfileScreen extends StatelessWidget {
  final bool isTab;
  const ProfileScreen({super.key, this.isTab = false});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: isTab
            ? null
            : IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.black),
                onPressed: () => Navigator.pop(context),
              ),
        title: const Text(
          "Patient Profile",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        centerTitle: true,
        actions: [
          TextButton(
            onPressed: () {},
            child: const Text(
              "Edit",
              style: TextStyle(
                color: AppColors.primary,
                fontWeight: FontWeight.bold,
                fontSize: 16,
              ),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
        child: Column(
          children: [
            // Profile Image
            Center(
              child: Stack(
                children: [
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: AppColors.primary, width: 2),
                      image: const DecorationImage(
                        image: NetworkImage('https://i.pravatar.cc/150?img=1'),
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: const BoxDecoration(
                        color: Color(0xFFC5E1A5), // Light Green
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(
                        Icons.camera_alt_outlined,
                        color: Colors.white,
                        size: 20,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              "Micah Chukwuemeka",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              "ID: #MED-882190",
              style: TextStyle(color: Colors.grey[600], fontSize: 14),
            ),
            const SizedBox(height: 32),

            // Vitals Grid
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.1,
              children: [
                VitalsCard(
                  title: "A+",
                  subtitle: "Blood Group",
                  icon: Icons.water_drop_outlined,
                  iconColor: AppColors.primary,
                  iconBackgroundColor: AppColors.primaryVariant,
                  backgroundColor: Colors.white,
                ),
                VitalsCard(
                  title: "AA",
                  subtitle: "Genotype",
                  icon: Icons.fingerprint, // Replaced science icon
                  iconColor: Colors.grey,
                  iconBackgroundColor: Color(0xFFF5F5F5),
                  backgroundColor: Colors.white,
                ),
                VitalsCard(
                  title: "68 kg",
                  subtitle: "Weight",
                  icon: Icons.scale, // Placeholder for weight
                  iconColor: AppColors.primary, // Using primary color
                  iconBackgroundColor: AppColors.primaryVariant,
                  backgroundColor: Colors.white,
                ),
                VitalsCard(
                  title: "170 cm",
                  subtitle: "Height",
                  icon: Icons.height, // Placeholder for height
                  iconColor: AppColors.primary,
                  iconBackgroundColor: AppColors.primaryVariant,
                  backgroundColor: Colors.white,
                ),
              ],
            ),
            const SizedBox(height: 32),

            // Personal Details
            _buildSectionHeader("Personal Details", Icons.person_outline),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.grey.withOpacity(0.1)),
              ),
              child: Column(
                children: [
                  _buildDetailRow("Date of Birth", "30 May, 2000"),
                  const Divider(height: 24, thickness: 0.5),
                  _buildDetailRow("Gender", "Female"),
                  const Divider(height: 24, thickness: 0.5),
                  _buildDetailRow("Address", "42 Ozubulu Street"),
                ],
              ),
            ),
            const SizedBox(height: 32),

            // Medical Alerts
            _buildSectionHeader("Medical Alerts", Icons.warning_amber_rounded),
            const SizedBox(height: 16),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.grey.withOpacity(0.1)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "ALLERGIES",
                    style: TextStyle(
                      color: Colors.grey[500],
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      _buildChip(
                        "Peanuts (High Risk)",
                        AppColors.redBackground,
                        AppColors.redAccent,
                      ),
                      const SizedBox(width: 8),
                      _buildChip(
                        "Penicillin",
                        const Color(0xFFFFF3E0),
                        Colors.orange,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "CHRONIC CONDITIONS",
                    style: TextStyle(
                      color: Colors.grey[500],
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      _buildChip(
                        "Asthma",
                        const Color(0xFFE0F2F1),
                        const Color(0xFF009688),
                      ),
                      const SizedBox(width: 8),
                      _buildChip(
                        "Hypertension",
                        const Color(0xFFE0F2F1),
                        const Color(0xFF009688),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),

            // Emergency Contact
            _buildSectionHeader(
              "Emergency Contact",
              Icons.contact_phone_outlined,
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.grey.withOpacity(0.1)),
              ),
              child: Row(
                children: [
                  Container(
                    width: 50,
                    height: 50,
                    decoration: const BoxDecoration(
                      color: Color(0xFFE3E4E6),
                      shape: BoxShape.circle,
                    ),
                    child: const Center(
                      child: Text(
                        "MC",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF5E6066),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          "Mike Chukwuemeka",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                        Text(
                          "Spouse",
                          style: TextStyle(
                            color: Colors.grey[600],
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: const BoxDecoration(
                      color: Color(0xFFE0F2F1),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.phone, color: Color(0xFF009688)),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: AppColors.primary),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
      ],
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 15)),
        Text(
          value,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
        ),
      ],
    );
  }

  Widget _buildChip(String label, Color backgroundColor, Color textColor) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: textColor,
          fontWeight: FontWeight.w600,
          fontSize: 13,
        ),
      ),
    );
  }
}
