import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/theme/app_colors.dart';
import 'dart:ui' as ui;
import 'upload_confirmation_screen.dart';
import '../../../../features/history/data/models/medical_history_model.dart';
import '../../../../features/home/presentation/providers/home_data_provider.dart';

class UploadResultScreen extends ConsumerStatefulWidget {
  const UploadResultScreen({super.key});

  @override
  ConsumerState<UploadResultScreen> createState() => _UploadResultScreenState();
}

class _UploadResultScreenState extends ConsumerState<UploadResultScreen> {
  final TextEditingController _testNameController = TextEditingController();
  final TextEditingController _dateController = TextEditingController();
  final TextEditingController _facilityController = TextEditingController();
  final TextEditingController _doctorController = TextEditingController();

  List<File> _selectedImages = [];
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage(ImageSource source) async {
    if (source == ImageSource.gallery) {
      final List<XFile> images = await _picker.pickMultiImage();
      if (images.isNotEmpty) {
        setState(() {
          _selectedImages.addAll(images.map((img) => File(img.path)));
        });
      }
    } else {
      final XFile? image = await _picker.pickImage(source: source);
      if (image != null) {
        setState(() {
          _selectedImages.add(File(image.path));
        });
      }
    }
  }

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
              iconColor: const Color(0xFF7C4DFF), // Purple calendar icon
            ),
            const SizedBox(height: 20),

            // Performing Facility
            _buildLabel("Performing Facility"),
            const SizedBox(height: 8),
            _buildTextField(
              controller: _facilityController,
              hintText: "e.g., Garki General Hospital",
              suffixIcon: Icons.location_on_outlined,
              iconColor: const Color(0xFF2962FF), // Blue location icon
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

            if (_selectedImages.isNotEmpty) ...[
              SizedBox(
                height: 100,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  itemCount: _selectedImages.length,
                  separatorBuilder: (context, index) =>
                      const SizedBox(width: 12),
                  itemBuilder: (context, index) {
                    return Stack(
                      children: [
                        Container(
                          height: 100,
                          width: 100,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(12),
                            image: DecorationImage(
                              image: FileImage(_selectedImages[index]),
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Positioned(
                          top: 4,
                          right: 4,
                          child: GestureDetector(
                            onTap: () {
                              setState(() {
                                _selectedImages.removeAt(index);
                              });
                            },
                            child: Container(
                              padding: const EdgeInsets.all(4),
                              decoration: const BoxDecoration(
                                color: Colors.black54,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.close,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                          ),
                        ),
                      ],
                    );
                  },
                ),
              ),
              const SizedBox(height: 20),
            ],

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildAttachmentOption(
                  icon: Icons.upload_file,
                  label: "Upload",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                  onTap: () => _pickImage(ImageSource.gallery),
                ),
                _buildAttachmentOption(
                  icon: Icons.camera_alt_outlined,
                  label: "Camera",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                  onTap: () => _pickImage(ImageSource.camera),
                ),
                _buildAttachmentOption(
                  icon: Icons.mic_none_outlined,
                  label: "Voice Note",
                  circleColor: const Color(0xFFE8F5E9),
                  iconColor: const Color(0xFF00C853),
                  onTap: () {}, // Not implemented yet
                ),
              ],
            ),

            const SizedBox(height: 40),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  // Create new item
                  final newItem = MedicalHistoryItem(
                    date: DateTime.now(),
                    title: _facilityController.text.isNotEmpty
                        ? _facilityController.text
                        : "Unknown Facility",
                    subtitle: _doctorController.text.isNotEmpty
                        ? _doctorController.text
                        : "Unknown Doctor",
                    description:
                        "Lab Result: ${_testNameController.text.isNotEmpty ? _testNameController.text : "Unnamed Test"}",
                    actionText: "VIEW LAB RESULTS (${_selectedImages.length})",
                    type: "diagnosis",
                  );

                  // Add to repository
                  ref.read(homeRepositoryProvider).addMedicalHistory(newItem);

                  // Refresh provider
                  ref.invalidate(medicalHistoryProvider);

                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const UploadConfirmationScreen(),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary, // Green color
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
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
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
      ),
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
