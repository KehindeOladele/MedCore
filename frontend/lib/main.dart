import 'package:flutter/material.dart';
import 'package:medcore/core/theme/app_theme.dart';
import 'package:medcore/features/home/presentation/pages/home_screen.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:medcore/core/data/hive_adapters.dart';
import 'package:medcore/features/home/data/adapters/reminder_model_adapter.dart';
import 'package:medcore/features/home/data/adapters/prescription_model_adapter.dart';
import 'package:medcore/features/home/data/models/reminder_model.dart';
import 'package:medcore/features/home/data/models/prescription_model.dart';
import 'package:medcore/features/profile/data/adapters/menstrual_cycle_model_adapter.dart';
import 'package:medcore/core/services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();

  Hive.registerAdapter(ColorAdapter());
  Hive.registerAdapter(IconDataAdapter());
  Hive.registerAdapter(ReminderModelAdapter());
  Hive.registerAdapter(PrescriptionModelAdapter());
  Hive.registerAdapter(MenstrualCycleModelAdapter());

  await Hive.openBox<ReminderModel>('reminders');
  await Hive.openBox<PrescriptionModel>('prescriptions');

  // Initialize Notifications
  final notificationService = NotificationService();
  await notificationService.init();

  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MedCore',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const HomeScreen(),
    );
  }
}
