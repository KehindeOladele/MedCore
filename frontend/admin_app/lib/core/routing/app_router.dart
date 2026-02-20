import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/pages/splash_screen.dart';
import '../../features/auth/presentation/pages/login_screen.dart';
import '../../features/auth/presentation/pages/role_selection_screen.dart';
import '../../features/dashboard/presentation/pages/dashboard_screen.dart';
import '../../features/patient_records/presentation/pages/patient_records_screen.dart';
import '../../features/patient_history/presentation/pages/patient_history_screen.dart';
import '../../features/data_capture/presentation/pages/add_clinical_note_screen.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(path: '/', builder: (context, state) => const SplashScreen()),
      GoRoute(
        path: '/role_selection',
        builder: (context, state) => const RoleSelectionScreen(),
      ),
      GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
      GoRoute(
        path: '/dashboard',
        builder: (context, state) => const DashboardScreen(),
      ),
      GoRoute(
        path: '/patient_records',
        builder: (context, state) => const PatientRecordsScreen(),
      ),
      GoRoute(
        path: '/patient_history',
        builder: (context, state) => const PatientHistoryScreen(),
      ),
      GoRoute(
        path: '/add_clinical_note',
        builder: (context, state) => const AddClinicalNoteScreen(),
      ),
      // Add more routes here as we build them out
    ],
  );
}
