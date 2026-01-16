import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/theme/app_colors.dart';
import '../widgets/vitals_card.dart';
import '../widgets/reminder_card.dart';
import '../widgets/prescription_card.dart';
import '../widgets/activity_item.dart';
import '../providers/home_controller.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Watch the provider to rebuild when index changes
    final currentIndex = ref.watch(homeIndexProvider);

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
                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 2,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                    childAspectRatio: 1.1,
                    children: const [
                      VitalsCard(
                        title: "A+",
                        subtitle: "Blood Group",
                        icon: Icons.water_drop_outlined,
                        iconColor: AppColors.primary,
                        iconBackgroundColor: AppColors.primaryVariant,
                      ),
                      VitalsCard(
                        title: "AA",
                        subtitle: "Genotype",
                        icon: Icons.fingerprint,
                        iconColor: Colors.grey,
                        iconBackgroundColor: Color(0xFFF5F5F5),
                      ),
                      VitalsCard(
                        title: "Penicillin",
                        subtitle: "Allergies",
                        icon: Icons.warning_amber_rounded,
                        iconColor: AppColors.redAccent,
                        iconBackgroundColor: AppColors.redBackground,
                        backgroundColor: AppColors.redBackground,
                        showChevron: true,
                      ),
                      VitalsCard(
                        title: "Set",
                        subtitle: "Reminder",
                        icon: Icons.medical_services_outlined,
                        iconColor: Color(0xFF009688),
                        iconBackgroundColor: Color(0xFFE0F2F1), // Teal variant
                      ),
                    ],
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
                  SizedBox(
                    height: 100, // Fixed height for horizontal list
                    child: ListView(
                      scrollDirection: Axis.horizontal,
                      children: [
                        const ReminderCard(),
                        const SizedBox(width: 16),
                        // Placeholder for second reminder
                        Container(
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
                        ),
                      ],
                    ),
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
                  const ActivityItem(
                    title: "General Checkup",
                    subtitle: "General Hospital • Dr. Isreal",
                    date: "Oct 24",
                    icon: Icons.monitor_heart,
                    iconColor: AppColors.primary,
                    iconBackgroundColor: AppColors.primaryVariant,
                  ),
                  const ActivityItem(
                    title: "Blood Test Results",
                    subtitle: "Lab Corp • Complete Panel",
                    date: "Oct 20",
                    icon: Icons
                        .water_drop, // Using water drop as kidneys replacement for now
                    iconColor: Color(0xFF009688), // Tealish
                    iconBackgroundColor: Color(0xFFE0F2F1),
                  ),
                  const ActivityItem(
                    title: "Flu Vaccination",
                    subtitle: "Garki Clinic",
                    date: "Sep 15",
                    icon: Icons.vaccines,
                    iconColor: AppColors.blueAccent,
                    iconBackgroundColor: AppColors.blueBackground,
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
