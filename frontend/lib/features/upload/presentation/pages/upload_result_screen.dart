import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../../../../core/theme/app_colors.dart';
import 'dart:ui' as ui;
import 'upload_confirmation_screen.dart';

class UploadResultScreen extends StatefulWidget {
  const UploadResultScreen({super.key});

  @override
  State<UploadResultScreen> createState() => _UploadResultScreenState();
}

class _UploadResultScreenState extends State<UploadResultScreen> {
  final TextEditingController _testNameController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();
  final TextEditingController _facilityController = TextEditingController();
  final TextEditingController _doctorController = TextEditingController();

  @override
  void dispose() {
    _testNameController.dispose();
    _dateController.dispose();
    _facilityController.dispose();
    _doctorController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          "Upload Result",
          style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text(
              "Cancel",
              style: TextStyle(color: Colors.grey, fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Lab Test Details",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),

            // Lab Test Name
            _buildLabel("Lab Test Name"),
            const SizedBox(height: 8),
            _buildTextField(
              controller: _testNameController,
              hintText: "e.g., Lipid Profile, CBC",
            ),
            const SizedBox(height: 20),

            // Date of Test
            _buildLabel("Date of Test"),
            const SizedBox(height: 8),
            _buildTextField(
              controller: _dateController,
              hintText: "DD/MM/YYYY",
              suffixIcon: Icons.calendar_today_outlined,
              iconColor: const Color(0xFF00C853), // Green calendar icon
            ),
            const SizedBox(height: 20),

            // Performing Facility
            _buildLabel("Performing Facility"),
            const SizedBox(height: 8),
            _buildTextField(
              controller: _facilityController,
              hintText: "e.g., Garki General Hospital",
              suffixIcon: Icons.location_on_outlined,
              iconColor: const Color(0xFF00C853), // Green location icon
            ),
            const SizedBox(height: 20),

            // Ordering Doctor
            _buildLabel("Ordering Doctor"),
            const SizedBox(height: 8),
            _buildTextField(
              controller: _doctorController,
              hintText: "e.g., Dr. Kehinde",
              // Use SVG for doctor icon
              suffixSvg: 'assets/icons/Vector.svg',
              iconColor: const Color(0xFF00C853),
            ),
            const SizedBox(height: 32),

            // Attachments
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Attachments",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFE8F5E9), // Light green
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: const Text(
                    "Required",
                    style: TextStyle(
                      color: Color(0xFF2E7D32),
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            const Text(
              "Upload a clear image or PDF of your official lab report.",
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 20),

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildAttachmentOption(
                  icon: Icons.upload_file,
                  label: "Upload",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                ),
                _buildAttachmentOption(
                  icon: Icons.camera_alt_outlined,
                  label: "Camera",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                ),
                _buildAttachmentOption(
                  icon: Icons.mic_none_outlined,
                  label: "Voice Note",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                ),
              ],
            ),

            const SizedBox(height: 40),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const UploadConfirmationScreen(),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF009688), // Teal color
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(25),
                  ),
                  elevation: 0,
                ),
                child: const Text(
                  "Save to Records",
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
    );
  }

  Widget _buildLabel(String text) {
    return Text(
      text,
      style: const TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        color: Colors.black87,
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hintText,
    IconData? suffixIcon,
    String? suffixSvg,
    Color? iconColor,
  }) {
    return TextField(
      controller: controller,
      decoration: InputDecoration(
        hintText: hintText,
        hintStyle: TextStyle(color: Colors.grey[400]),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 16,
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
        filled: true,
        fillColor: const Color(0xFFFAFAFA), // Very light grey bg
        suffixIcon: suffixSvg != null
            ? Padding(
                padding: const EdgeInsets.all(12.0),
                child: SvgPicture.asset(
                  suffixSvg,
                  colorFilter: iconColor != null
                      ? ColorFilter.mode(iconColor, BlendMode.srcIn)
                      : null,
                ),
              )
            : (suffixIcon != null
                  ? Icon(suffixIcon, color: iconColor ?? Colors.grey)
                  : null),
      ),
    );
  }

  Widget _buildAttachmentOption({
    required IconData icon,
    required String label,
    Color? circleColor,
    Color? iconColor,
  }) {
    return Column(
      children: [
        CustomPaint(
          painter: DashedBorderPainter(),
          child: Container(
            width: 80,
            height: 80,
            alignment: Alignment.center,
            child: Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: circleColor ?? const Color(0xFFE8F5E9),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: iconColor, size: 24),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w500,
            color: Colors.black,
          ),
        ),
      ],
    );
  }
}

class DashedBorderPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()
      ..color = Colors.grey.withOpacity(0.5)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    const double dashWidth = 4;
    const double dashSpace = 4;
    final RRect rrect = RRect.fromRectAndRadius(
      Rect.fromLTWH(0, 0, size.width, size.height),
      const Radius.circular(16),
    );

    final Path path = Path()..addRRect(rrect);

    // Simple dash logic for RRect
    Path dashPath = Path();
    double distance = 0.0;

    for (ui.PathMetric pathMetric in path.computeMetrics()) {
      while (distance < pathMetric.length) {
        dashPath.addPath(
          pathMetric.extractPath(distance, distance + dashWidth),
          Offset.zero,
        );
        distance += dashWidth;
        distance += dashSpace;
      }
    }
    canvas.drawPath(dashPath, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}
