import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../widgets/vitals_card.dart';
import '../widgets/reminder_card.dart';
import '../widgets/prescription_card.dart';
import '../widgets/activity_item.dart';
import '../widgets/flow_vital_card.dart';
import '../../data/models/vital_model.dart';
import '../../data/models/prescription_model.dart';
import '../../data/models/user_summary_model.dart';

import '../providers/home_controller.dart';
import '../providers/home_data_provider.dart';
import '../../../profile/presentation/providers/profile_provider.dart';

import '../../../allergies/presentation/pages/allergies_screen.dart';
import '../../../reminders/presentation/pages/add_reminder_screen.dart';
import '../../../reminders/presentation/pages/reminders_screen.dart';
import '../../../profile/presentation/pages/profile_screen.dart';
import '../../../history/presentation/pages/medical_history_screen.dart';
import '../../../history/presentation/pages/medical_records_screen.dart';
import '../../../upload/presentation/pages/new_upload_screen.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch the provider to rebuild when index changes
    final currentIndex = ref.watch(homeIndexProvider);
    final vitalsAsync = ref.watch(vitalsProvider);
    final remindersAsync = ref.watch(remindersProvider);
    final activityAsync = ref.watch(recentActivityProvider);
    final prescriptionsAsync = ref.watch(prescriptionsProvider);
    final summaryAsync = ref.watch(userSummaryProvider);
    final profileAsync = ref.watch(profileProvider);
    final fallbackIsFemale = ref.watch(genderProvider);
    final isFemale = profileAsync.maybeWhen(
      data: (profile) => profile.gender?.toLowerCase() == 'female',
      orElse: () => fallbackIsFemale,
    );

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: currentIndex == 0
          ? AppBar(
              title: Row(
                children: [
                  // Avatar: use real API avatar if available
                  summaryAsync.when(
                    data: (summary) => CircleAvatar(
                      backgroundImage: summary.avatarUrl != null
                          ? NetworkImage(summary.avatarUrl!)
                          : NetworkImage(
                              isFemale
                                  ? 'https://i.pravatar.cc/150?img=1'
                                  : 'https://i.pravatar.cc/150?img=11',
                            ),
                    ),
                    loading: () => CircleAvatar(
                      backgroundImage: NetworkImage(
                        isFemale
                            ? 'https://i.pravatar.cc/150?img=1'
                            : 'https://i.pravatar.cc/150?img=11',
                      ),
                    ),
                    error: (_, __) => const CircleAvatar(
                      child: Icon(Icons.person),
                    ),
                  ),
                  const SizedBox(width: 12),
                  // Name: use real name from API
                  summaryAsync.when(
                    data: (summary) => Text(
                      'Hello, ${summary.fullName.split(' ').first}',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    loading: () => Text(
                      'Hello!',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    error: (_, __) => Text(
                      'Hello!',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              actions: [
                IconButton(
                  icon: const Icon(Icons.notifications_outlined),
                  onPressed: () {},
                ),
                const SizedBox(width: 8),
              ],
            )
          : null,
      body: IndexedStack(
        index: currentIndex,
        children: [
          // Index 0: Home
          SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 24),
                  // Vitals Section
                  Text(
                    "My Vitals",
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  // Vitals: prefer live API data, fall back to Hive/mock
                  summaryAsync.when(
                    data: (summary) => _buildVitalsGrid(
                      context,
                      summary,
                      isFemale,
                      ref,
                      vitalsAsync,
                    ),
                    loading: () => vitalsAsync.when(
                      data: (vitals) =>
                          _buildVitalsFromLocal(context, vitals),
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text('Error: $e'),
                    ),
                    error: (_, __) => vitalsAsync.when(
                      data: (vitals) =>
                          _buildVitalsFromLocal(context, vitals),
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text('Error: $e'),
                    ),
                  ),

                  const SizedBox(height: 32),

                  // Reminders Section
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Reminders",
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const RemindersScreen(),
                            ),
                          );
                        },
                        child: Text(
                          "See All",
                          style: TextStyle(
                            color: AppColors.primary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  remindersAsync.when(
                    data: (reminders) {
                      if (reminders.isEmpty) {
                        return Container(
                          height: 140,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.surface,
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.notifications_off_outlined,
                                color: Colors.grey,
                                size: 40,
                              ),
                              const SizedBox(height: 8),
                              Text(
                                "No reminders set",
                                style: TextStyle(color: Colors.grey[600]),
                              ),
                            ],
                          ),
                        );
                      }
                      return SizedBox(
                        height: 140,
                        child: ListView.separated(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          itemCount: reminders.length,
                          separatorBuilder: (context, index) =>
                              const SizedBox(width: 16),
                          itemBuilder: (context, index) {
                            return ReminderCard(reminder: reminders[index]);
                          },
                        ),
                      );
                    },
                    loading: () =>
                        const Center(child: CircularProgressIndicator()),
                    error: (err, stack) => Text('Error: $err'),
                  ),
                  const SizedBox(height: 32),

                  // Prescriptions Section
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Ongoing Prescriptions",
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const MedicalRecordsScreen(
                                initialTab: "Prescriptions",
                              ),
                            ),
                          );
                        },
                        child: Text(
                          "Manage",
                          style: TextStyle(
                            color: AppColors.primary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const SizedBox(height: 8),
                  // Prescriptions: prefer live API data, fall back to local
                  summaryAsync.when(
                    data: (summary) => _buildApiPrescriptions(
                      context,
                      summary.activePrescriptions,
                    ),
                    loading: () => prescriptionsAsync.when(
                      data: (list) => _buildLocalPrescriptions(context, list),
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text('Error: $e'),
                    ),
                    error: (_, __) => prescriptionsAsync.when(
                      data: (list) => _buildLocalPrescriptions(context, list),
                      loading: () =>
                          const Center(child: CircularProgressIndicator()),
                      error: (e, _) => Text('Error: $e'),
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Recent Activity Section
                  Text(
                    "Recent Activity",
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  activityAsync.when(
                    data: (activities) {
                      if (activities.isEmpty) {
                        return Container(
                          padding: const EdgeInsets.all(32),
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.surface,
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            children: [
                              Icon(Icons.history, color: Colors.grey, size: 48),
                              const SizedBox(height: 16),
                              Text(
                                "No activities yet",
                                style: TextStyle(
                                  color: Colors.grey[600],
                                  fontSize: 16,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ],
                          ),
                        );
                      }
                      return Column(
                        children: activities
                            .map(
                              (activity) => ActivityItem(
                                title: activity.title,
                                subtitle: activity.subtitle,
                                date: activity.date,
                                icon: activity.icon,
                                iconColor: activity.iconColor,
                                iconBackgroundColor:
                                    activity.iconBackgroundColor,
                              ),
                            )
                            .toList(),
                      );
                    },
                    loading: () =>
                        const Center(child: CircularProgressIndicator()),
                    error: (err, stack) => Text('Error: $err'),
                  ),
                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
          // Index 1: History
          const MedicalHistoryScreen(),
          // Index 2: Add Record
          const NewUploadScreen(isTab: true),
          // Index 3: Profile
          const ProfileScreen(isTab: true),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: Colors.grey,
        showUnselectedLabels: true,
        currentIndex: currentIndex,
        onTap: (index) {
          // Update state using the provider
          ref.read(homeIndexProvider.notifier).setIndex(index);
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.grid_view), label: 'Home'),
          BottomNavigationBarItem(
            icon: Icon(Icons.folder_outlined),
            label: 'History',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add_circle, size: 40),
            label: 'Add Record',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person_outline),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}

// ── Helper builders ───────────────────────────────────────────────────────────

/// Builds the vitals grid from the live API summary, using the menstrual cycle
/// vital from the local provider to preserve that flow-day logic.
Widget _buildVitalsGrid(
  BuildContext context,
  UserSummaryModel summary,
  bool isFemale,
  WidgetRef ref,
  AsyncValue<List<VitalModel>> vitalsAsync,
) {
  final vitals = summary.vitals;

  // Build the list of VitalModel cards from the real API values
  final apiVitals = <VitalModel>[
    VitalModel(
      title: vitals.bloodGroup ?? '—',
      subtitle: 'Blood Group',
      icon: Icons.water_drop_outlined,
      iconColor: AppColors.primary,
      iconBackgroundColor: AppColors.primaryVariant,
      secondaryTitle: vitals.genotype,
      secondarySubtitle: vitals.genotype != null ? 'Genotype' : null,
    ),
    if (vitals.genotype != null && vitals.bloodGroup != null)
      VitalModel(
        title: vitals.genotype!,
        subtitle: 'Genotype',
        icon: Icons.fingerprint,
        iconColor: Colors.grey,
        iconBackgroundColor: const Color(0xFFF5F5F5),
      ),
    VitalModel(
      title: vitals.allergies.isNotEmpty
          ? vitals.allergies.first
          : 'None',
      subtitle: 'Allergies',
      icon: Icons.warning_amber_rounded,
      iconColor: AppColors.redAccent,
      iconBackgroundColor: Colors.white,
      backgroundColor: AppColors.redBackground,
      showChevron: true,
      titleColor: AppColors.redAccent,
    ),
    const VitalModel(
      title: 'Set',
      subtitle: 'Reminder',
      icon: Icons.medical_services_outlined,
      iconColor: Color(0xFF009688),
      iconBackgroundColor: Colors.white,
      backgroundColor: Color(0xFFE0F2F1),
      titleColor: Color(0xFF009688),
    ),
  ];

  // If female, try to inject the flow card from the local provider
  final displayVitals = isFemale
      ? vitalsAsync.maybeWhen(
          data: (localVitals) {
            final flowCard = localVitals.where((v) => v.isFlow).firstOrNull;
            if (flowCard != null) {
              return [apiVitals[0], flowCard, apiVitals[2], apiVitals[3]];
            }
            return apiVitals;
          },
          orElse: () => apiVitals,
        )
      : apiVitals;

  return _buildVitalsFromLocal(context, displayVitals);
}

Widget _buildVitalsFromLocal(BuildContext context, List<VitalModel> vitals) {
  return GridView.count(
    shrinkWrap: true,
    physics: const NeverScrollableScrollPhysics(),
    crossAxisCount: 2,
    crossAxisSpacing: 16,
    mainAxisSpacing: 16,
    childAspectRatio: 1.1,
    children: vitals.map((vital) {
      if (vital.isFlow) return FlowVitalCard(vital: vital);
      return VitalsCard(
        title: vital.title,
        subtitle: vital.subtitle,
        icon: vital.icon,
        iconColor: vital.iconColor,
        iconBackgroundColor: vital.iconBackgroundColor,
        backgroundColor: vital.backgroundColor ?? Colors.white,
        showChevron: vital.showChevron,
        onTap: () {
          if (vital.subtitle == 'Allergies') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const AllergiesScreen(),
              ),
            );
          } else if (vital.subtitle == 'Reminder') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const AddReminderScreen(),
              ),
            );
          } else if (vital.subtitle == 'Blood Group') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => const ProfileScreen(),
              ),
            );
          }
        },
        titleColor: vital.titleColor,
        secondaryTitle: vital.secondaryTitle,
        secondarySubtitle: vital.secondarySubtitle,
      );
    }).toList(),
  );
}

Widget _buildApiPrescriptions(
  BuildContext context,
  List<ActivePrescriptionModel> prescriptions,
) {
  if (prescriptions.isEmpty) {
    return _emptyPrescriptions(context);
  }
  return ListView.separated(
    shrinkWrap: true,
    physics: const NeverScrollableScrollPhysics(),
    itemCount: prescriptions.length,
    separatorBuilder: (_, __) => const SizedBox(height: 16),
    itemBuilder: (context, index) {
      final p = prescriptions[index];
      // Map to the existing PrescriptionModel widget shape
      final localModel = PrescriptionModel(
        id: p.id,
        title: p.drugName,
        subtitle: p.category ?? 'Medication',
        dosage: p.dosage ?? '—',
        schedule: p.schedule ?? '—',
        icon: Icons.medication_outlined,
      );
      return PrescriptionCard(prescription: localModel, onTap: () {});
    },
  );
}

Widget _buildLocalPrescriptions(
  BuildContext context,
  List<PrescriptionModel> prescriptions,
) {
  if (prescriptions.isEmpty) return _emptyPrescriptions(context);
  return ListView.separated(
    shrinkWrap: true,
    physics: const NeverScrollableScrollPhysics(),
    itemCount: prescriptions.length,
    separatorBuilder: (_, __) => const SizedBox(height: 16),
    itemBuilder: (context, index) => PrescriptionCard(
      prescription: prescriptions[index],
      onTap: () {},
    ),
  );
}

Widget _emptyPrescriptions(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(32),
    alignment: Alignment.center,
    decoration: BoxDecoration(
      color: Theme.of(context).colorScheme.surface,
      borderRadius: BorderRadius.circular(16),
    ),
    child: Column(
      children: [
        const Icon(Icons.medication_outlined, color: Colors.grey, size: 48),
        const SizedBox(height: 16),
        Text(
          'No active prescriptions',
          style: TextStyle(
            color: Colors.grey[600],
            fontSize: 16,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    ),
  );
}
