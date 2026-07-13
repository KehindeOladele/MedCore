import 'package:flutter/material.dart';
import 'package:medcore/core/theme/app_theme.dart';
import 'package:medcore/core/theme/theme_provider.dart';
import 'package:medcore/features/home/presentation/pages/home_screen.dart';
import 'package:medcore/features/auth/presentation/pages/splash_screen.dart';
import 'package:medcore/features/auth/presentation/pages/sign_up_screen.dart';
import 'package:medcore/features/auth/presentation/pages/email_verification_screen.dart';
import 'package:medcore/features/auth/presentation/pages/gender_selection_screen.dart';
import 'package:medcore/features/auth/presentation/pages/patient_login_screen.dart';
import 'package:medcore/features/auth/presentation/pages/welcome_screen.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:medcore/core/data/hive_adapters.dart';
import 'package:medcore/features/home/data/adapters/reminder_model_adapter.dart';
import 'package:medcore/features/home/data/adapters/prescription_model_adapter.dart';
import 'package:medcore/features/home/data/models/reminder_model.dart';
import 'package:medcore/features/home/data/models/prescription_model.dart';
import 'package:medcore/features/profile/data/adapters/menstrual_cycle_model_adapter.dart';
import 'package:medcore/features/allergies/data/adapters/allergy_model_adapter.dart';
import 'package:medcore/features/allergies/data/models/allergy_model.dart';
import 'package:medcore/features/history/data/adapters/medical_history_item_adapter.dart';
import 'package:medcore/features/history/data/models/medical_history_model.dart';
import 'package:medcore/core/services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();

  Hive.registerAdapter(ColorAdapter());
  Hive.registerAdapter(IconDataAdapter());
  Hive.registerAdapter(ReminderModelAdapter());
  Hive.registerAdapter(PrescriptionModelAdapter());
  Hive.registerAdapter(MenstrualCycleModelAdapter());
  Hive.registerAdapter(AllergyModelAdapter());
  Hive.registerAdapter(MedicalHistoryItemAdapter());

  await Hive.openBox<ReminderModel>('reminders');
  await Hive.openBox<PrescriptionModel>('prescriptions');
  await Hive.openBox<AllergyModel>('local_allergies');
  await Hive.openBox<MedicalHistoryItem>('local_history');
  await Hive.openBox('settings');

  // Initialize Notifications
  final notificationService = NotificationService();
  await notificationService.init();

  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);
    
    return MaterialApp(
      title: 'MedCore',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: themeMode,
      home: const SplashScreen(),
      routes: {
        '/splash': (context) => const SplashScreen(),
        '/sign_up': (context) => const SignUpScreen(),
        '/email_verification': (context) => const EmailVerificationScreen(),
        '/gender_selection': (context) => const GenderSelectionScreen(),
        '/patient_login': (context) => const PatientLoginScreen(),
        '/welcome': (context) => const WelcomeScreen(),
        '/home': (context) => const HomeScreen(),
      },
    );
  }
}
