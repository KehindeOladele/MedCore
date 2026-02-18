import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../widgets/vitals_card.dart';
import '../widgets/reminder_card.dart';
import '../widgets/prescription_card.dart';
import '../widgets/activity_item.dart';
import '../widgets/flow_vital_card.dart';

import '../providers/home_controller.dart';
import '../providers/home_data_provider.dart';

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

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: currentIndex == 0
          ? AppBar(
              title: Row(
                children: [
                  const CircleAvatar(
                    backgroundImage: NetworkImage(
                      'https://i.pravatar.cc/150?img=1',
                    ), // Placeholder
                  ),
                  const SizedBox(width: 12),
                  Text(
                    "Hello, Micah",
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              actions: [
                IconButton(
                  icon: Icon(
                    Icons.switch_account_outlined,
                    color: AppColors.primary,
                  ),
                  onPressed: () {
                    ref.read(genderProvider.notifier).toggleGender();
                  },
                ),
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
                  vitalsAsync.when(
                    data: (vitals) => GridView.count(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      crossAxisCount: 2,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                      childAspectRatio: 1.1,
                      children: vitals.map((vital) {
                        if (vital.isFlow) {
                          return FlowVitalCard(vital: vital);
                        }
                        return VitalsCard(
                          title: vital.title,
                          subtitle: vital.subtitle,
                          icon: vital.icon,
                          iconColor: vital.iconColor,
                          iconBackgroundColor: vital.iconBackgroundColor,
                          backgroundColor:
                              vital.backgroundColor ?? Colors.white,
                          showChevron: vital.showChevron,
                          onTap: () {
                            if (vital.subtitle == "Allergies") {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => const AllergiesScreen(),
                                ),
                              );
                            } else if (vital.subtitle == "Reminder") {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) =>
                                      const AddReminderScreen(),
                                ),
                              );
                            } else if (vital.subtitle == "Blood Group") {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => const ProfileScreen(),
                                ),
                              );
                            }
                          },
                          titleColor: vital.titleColor,
                          secondaryTitle: vital.secondaryTitle,
                          secondarySubtitle: vital.secondarySubtitle,
                        );
                      }).toList(),
                    ),
                    loading: () =>
                        const Center(child: CircularProgressIndicator()),
                    error: (err, stack) => Text('Error: $err'),
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
                            color: Colors.white,
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
                  prescriptionsAsync.when(
                    data: (prescriptions) {
                      if (prescriptions.isEmpty) {
                        return Container(
                          padding: const EdgeInsets.all(32),
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            children: [
                              Icon(
                                Icons.medication_outlined,
                                color: Colors.grey,
                                size: 48,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                "No prescription yet",
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
                      return ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: prescriptions.length,
                        separatorBuilder: (context, index) =>
                            const SizedBox(height: 16),
                        itemBuilder: (context, index) {
                          return PrescriptionCard(
                            prescription: prescriptions[index],
                          );
                        },
                      );
                    },
                    loading: () =>
                        const Center(child: CircularProgressIndicator()),
                    error: (err, stack) => Text('Error: $err'),
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
                    data: (activities) => Column(
                      children: activities
                          .map(
                            (activity) => ActivityItem(
                              title: activity.title,
                              subtitle: activity.subtitle,
                              date: activity.date,
                              icon: activity.icon,
                              iconColor: activity.iconColor,
                              iconBackgroundColor: activity.iconBackgroundColor,
                            ),
                          )
                          .toList(),
                    ),
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
