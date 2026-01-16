import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../widgets/vitals_card.dart';
import '../widgets/reminder_card.dart';
import '../widgets/prescription_card.dart';
import '../widgets/activity_item.dart';
import '../providers/home_controller.dart';
import '../providers/home_data_provider.dart';

import '../../../allergies/presentation/pages/allergies_screen.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch the provider to rebuild when index changes
    final currentIndex = ref.watch(homeIndexProvider);
    final vitalsAsync = ref.watch(vitalsProvider);
    final remindersAsync = ref.watch(remindersProvider);
    final activityAsync = ref.watch(recentActivityProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
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
              style: Theme.of(
                context,
              ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
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
      ),
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
                            }
                          },
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
                        onPressed: () {},
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
                    data: (reminders) => SizedBox(
                      height: 100, // Fixed height for horizontal list
                      child: ListView.separated(
                        scrollDirection: Axis.horizontal,
                        itemCount:
                            reminders.length +
                            1, // +1 for the placeholder/add button
                        separatorBuilder: (context, index) =>
                            const SizedBox(width: 16),
                        itemBuilder: (context, index) {
                          if (index < reminders.length) {
                            // Assuming ReminderCard takes data, but currently it's static.
                            // For now we just show the static card for each item to prove connection.
                            return const ReminderCard();
                          } else {
                            // The placeholder/add button
                            return Container(
                              width: 100,
                              alignment: Alignment.center,
                              decoration: BoxDecoration(
                                color: AppColors.surface,
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: const Icon(
                                Icons.medication,
                                color: AppColors.orangeAccent,
                              ),
                            );
                          }
                        },
                      ),
                    ),
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
                        onPressed: () {},
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
                  const PrescriptionCard(),
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
          const Center(child: Text("History")),
          // Index 2: Add Record
          const Center(child: Text("Add Record")),
          // Index 3: Profile
          const Center(child: Text("Profile")),
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
