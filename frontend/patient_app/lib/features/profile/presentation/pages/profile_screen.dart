import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/services/api_service.dart';
import '../../../home/presentation/providers/home_controller.dart';
import 'menstrual_cycle_screen.dart';
import 'log_period_screen.dart';

import '../providers/menstrual_cycle_provider.dart';
import '../providers/profile_provider.dart';
import '../widgets/profile_setup_form.dart';
import 'package:intl/intl.dart';
class ProfileScreen extends ConsumerStatefulWidget {
  final bool isTab;
  const ProfileScreen({super.key, this.isTab = false});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  bool _uploadingAvatar = false;

  Future<void> _pickAndUploadAvatar(BuildContext context) async {
    final messenger = ScaffoldMessenger.of(context); // capture before await
    final picker = ImagePicker();
    final picked = await picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 80,
    );
    if (picked == null) return;

    setState(() => _uploadingAvatar = true);
    try {
      final api = ref.read(apiServiceProvider);
      await api.postMultipart(
        '/patients/profile/upload-avatar',
        File(picked.path),
        fieldName: 'file',
      );
      ref.invalidate(profileProvider);
      messenger.showSnackBar(
        const SnackBar(
          content: Text('Profile photo updated!'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      messenger.showSnackBar(
        SnackBar(
          content: Text('Upload failed: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (mounted) setState(() => _uploadingAvatar = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final profileState = ref.watch(profileProvider);
    final fallbackIsFemale = ref.watch(genderProvider);
    final isFemale = profileState.maybeWhen(
      data: (profile) => profile.gender?.toLowerCase() == 'female',
      orElse: () => fallbackIsFemale,
    );

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: widget.isTab
            ? null
            : IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.black),
                onPressed: () => Navigator.pop(context),
              ),
        title: const Text(
          'Patient Profile',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        centerTitle: true,
        actions: [
          profileState.when(
            data: (profile) => TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => Scaffold(
                      appBar: AppBar(
                        title: const Text(
                          'Edit Profile',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        centerTitle: true,
                        backgroundColor: Colors.white,
                        elevation: 0,
                        foregroundColor: Colors.black,
                      ),
                      backgroundColor: AppColors.background,
                      body: SingleChildScrollView(
                        child: ProfileSetupForm(profile: profile),
                      ),
                    ),
                  ),
                ).then((_) => ref.invalidate(profileProvider));
              },
              child: const Text(
                'Edit',
                style: TextStyle(
                  color: AppColors.primary,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
            ),
            loading: () => const SizedBox.shrink(),
            error: (_, __) => const SizedBox.shrink(),
          ),
        ],
      ),
      body: profileState.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text("Error: $err")),
        data: (profile) {
          final needsSetup = profile.firstName.isEmpty || 
                             profile.lastName.isEmpty || 
                             profile.bloodGroup == null || 
                             profile.gender == null;

          if (needsSetup) {
            return ProfileSetupForm(profile: profile);
          }

          final dob = profile.dateOfBirth != null 
              ? DateFormat('dd MMM, yyyy').format(profile.dateOfBirth!) 
              : 'Not set';

          return SingleChildScrollView(
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
                          image: DecorationImage(
                            image: NetworkImage(
                              profile.profileImageUrl ??
                              (isFemale
                                  ? 'https://i.pravatar.cc/150?img=1'
                                  : 'https://i.pravatar.cc/150?img=11'),
                            ),
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                        Positioned(
                          bottom: 0,
                          right: 0,
                          child: GestureDetector(
                            onTap: _uploadingAvatar
                                ? null
                                : () => _pickAndUploadAvatar(context),
                            child: Container(
                              padding: const EdgeInsets.all(8),
                              decoration: const BoxDecoration(
                                color: Color(0xFFC5E1A5),
                                shape: BoxShape.circle,
                              ),
                              child: _uploadingAvatar
                                  ? const SizedBox(
                                      width: 20,
                                      height: 20,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                        color: Colors.white,
                                      ),
                                    )
                                  : const Icon(
                                      Icons.camera_alt_outlined,
                                      color: Colors.white,
                                      size: 20,
                                    ),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  profile.fullName.isEmpty ? "Unknown Patient" : profile.fullName,
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(
                  "ID: #${profile.id.split('-').first.toUpperCase()}",
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
                  childAspectRatio: 1.5,
                  children: [
                    _buildVitalCard(
                      title: profile.bloodGroup ?? "--",
                      subtitle: "Blood Group",
                      icon: Icons.water_drop_outlined,
                      iconColor: AppColors.primary,
                      backgroundColor: Colors.white,
                    ),
                    _buildVitalCard(
                      title: profile.genotype ?? "--",
                      subtitle: "Genotype",
                      icon: Icons.science_outlined,
                      iconColor: AppColors.primary,
                      backgroundColor: Colors.white,
                    ),
                    _buildVitalCard(
                      title: profile.weight != null ? "${profile.weight} kg" : "--",
                      subtitle: "Weight",
                      icon: Icons.monitor_weight_outlined,
                      iconColor: AppColors.primary,
                      backgroundColor: Colors.white,
                    ),
                    _buildVitalCard(
                      title: profile.height != null ? "${profile.height} cm" : "--",
                      subtitle: "Height",
                      icon: Icons.height,
                      iconColor: AppColors.primary,
                      backgroundColor: Colors.white,
                    ),
                  ],
                ),
                const SizedBox(height: 32),

                // Menstrual Cycle Section (Conditional)
                if (isFemale) ...[
                  _buildMenstrualCycleSection(context, ref),
                  const SizedBox(height: 32),
                ],

                // Personal Details
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.withOpacity(0.1)),
                  ),
                  child: Column(
                    children: [
                      _buildDetailRow("Date of Birth", dob),
                      const Divider(height: 24, thickness: 0.5),
                      _buildDetailRow("Gender", profile.gender ?? (isFemale ? "Female" : "Male")),
                      const Divider(height: 24, thickness: 0.5),
                      _buildDetailRow("Address", profile.address ?? "Not provided"),
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
                          letterSpacing: 1.0,
                        ),
                      ),
                      const SizedBox(height: 12),
                      profile.allergies.isNotEmpty
                          ? Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: profile.allergies.map((allergy) {
                                return _buildChip(
                                  allergy,
                                  AppColors.redBackground,
                                  AppColors.redAccent,
                                );
                              }).toList(),
                            )
                          : Text("No known allergies", style: TextStyle(color: Colors.grey[600])),
                      const SizedBox(height: 24),
                      Text(
                        "CHRONIC CONDITIONS",
                        style: TextStyle(
                          color: Colors.grey[500],
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.0,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          _buildChip(
                            "None recorded",
                            AppColors.primaryVariant,
                            AppColors.primary,
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
                  child: profile.emergencyContactName != null
                    ? Row(
                        children: [
                          Container(
                            width: 50,
                            height: 50,
                            decoration: const BoxDecoration(
                              color: Color(0xFFE3E4E6),
                              shape: BoxShape.circle,
                            ),
                            child: Center(
                              child: Text(
                                profile.emergencyContactName!.substring(0, 2).toUpperCase(),
                                style: const TextStyle(
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
                                Text(
                                  profile.emergencyContactName!,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                                Text(
                                  profile.emergencyContactPhone ?? "No phone",
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
                              color: AppColors.primaryVariant,
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.phone, color: AppColors.primary),
                          ),
                        ],
                      )
                    : const Text("No emergency contact provided"),
                ),
                const SizedBox(height: 40),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildVitalCard({
    required String title,
    required String subtitle,
    required IconData icon,
    required Color iconColor,
    required Color backgroundColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.withOpacity(0.1)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 8,
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
              Text(
                subtitle, // "Blood Group" etc
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.grey[600],
                  fontWeight: FontWeight.w500,
                ),
              ),
              Icon(icon, color: iconColor.withOpacity(0.5), size: 18),
            ],
          ),
          Text(
            title, // "O+" etc
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Color(0xFF1A1C1E),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCycleInfo(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 10,
            color: Colors.grey,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1A1C1E),
          ),
        ),
      ],
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: Colors.grey[700], size: 20), // Updated to grey
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 18,
            color: Color(0xFF1A1C1E),
          ),
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
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
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

  Widget _buildMenstrualCycleSection(BuildContext context, WidgetRef ref) {
    final cycleAsync = ref.watch(menstrualCycleProvider);

    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                const Icon(Icons.water_drop, color: Colors.red),
                const SizedBox(width: 8),
                Text(
                  "Menstrual Cycle",
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: const Color(0xFF1A1C1E),
                  ),
                ),
              ],
            ),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const LogPeriodScreen(),
                  ),
                );
              },
              child: const Text(
                "Edit",
                style: TextStyle(
                  color: AppColors.primary,
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        cycleAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) => const Text("Failed to load cycle data"),
          data: (cycle) {
            if (cycle == null) {
              return GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const LogPeriodScreen(),
                    ),
                  );
                },
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.withOpacity(0.2)),
                  ),
                  child: Column(
                    children: const [
                      Icon(
                        Icons.calendar_today_outlined,
                        size: 40,
                        color: AppColors.primary,
                      ),
                      SizedBox(height: 12),
                      Text(
                        "Log your period to see cycle predictions",
                        style: TextStyle(color: Colors.grey),
                      ),
                    ],
                  ),
                ),
              );
            }

            final diff = DateTime.now().difference(cycle.lastPeriodDate).inDays;
            var currentDay = diff + 1;
            if (currentDay < 1) currentDay = 1;

            // Simple Phase Logic Reuse
            String phase = "Luteal Phase";
            double progress = currentDay / cycle.cycleLength;
            if (progress > 1.0) progress = 1.0;

            final ovulationDay = cycle.cycleLength - 14;

            if (currentDay <= cycle.periodLength) {
              phase = "Menstruation";
            } else if (currentDay < ovulationDay - 5) {
              phase = "Follicular Phase";
            } else if (currentDay <= ovulationDay) {
              phase = "Ovulation";
            } else {
              phase = "Luteal Phase";
            }

            final nextPeriodDays = cycle.cycleLength - currentDay;
            final daysText = nextPeriodDays < 0
                ? "Overdue"
                : "$nextPeriodDays Days";

            return GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const MenstrualCycleScreen(),
                  ),
                );
              },
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    // Circular Indicator
                    SizedBox(
                      width: 100,
                      height: 100,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          SizedBox(
                            width: 95,
                            height: 95,
                            child: CircularProgressIndicator(
                              value: progress,
                              strokeWidth: 8,
                              backgroundColor: Colors.grey[200],
                              valueColor: const AlwaysStoppedAnimation<Color>(
                                AppColors.primary,
                              ),
                            ),
                          ),
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text(
                                "Day",
                                style: TextStyle(
                                  fontSize: 10,
                                  color: Colors.grey,
                                ),
                              ),
                              Text(
                                "$currentDay",
                                style: const TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                phase,
                                style: const TextStyle(
                                  fontSize: 8,
                                  color: AppColors.primary,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildCycleInfo("NEXT\nPERIOD", daysText),
                              _buildCycleInfo(
                                "CYCLE\nLENGTH",
                                "${cycle.cycleLength} Days",
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton.icon(
                              onPressed: () {},
                              icon: const Icon(Icons.add, size: 16),
                              label: const Text("Log Symptoms"),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.primary,
                                foregroundColor: Colors.white,
                                elevation: 0,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
    );
  }
}
