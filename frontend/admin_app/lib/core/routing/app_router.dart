import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/data/providers/auth_controller.dart';
import '../../features/auth/presentation/pages/splash_screen.dart';
import '../../features/auth/presentation/pages/login_screen.dart';
import '../../features/auth/presentation/pages/role_selection_screen.dart';
import '../../features/dashboard/presentation/pages/dashboard_screen.dart';
import '../../features/patient_records/presentation/pages/patient_records_screen.dart';
import '../../features/patient_history/presentation/pages/patient_history_screen.dart';
import '../../features/data_capture/presentation/pages/add_clinical_note_screen.dart';
import '../../features/data_capture/presentation/pages/voice_dictation_screen.dart';
import '../../features/ai_categorization/presentation/pages/ai_categorization_screen.dart';
import '../../features/ai_categorization/presentation/pages/capture_screen.dart';
import '../../features/ai_categorization/presentation/pages/upload_confirmation_screen.dart';
import '../../features/ai_categorization/presentation/pages/ai_scan_result_screen.dart';
import '../../features/ai_categorization/presentation/pages/ai_categorization_result_screen.dart';
import '../../features/patient_records/presentation/pages/medical_records_screen.dart';
import '../../features/patient_records/presentation/pages/clinical_notes_screen.dart';
import '../../features/patient_records/presentation/pages/prescriptions_screen.dart';
import '../../features/patient_records/presentation/pages/add_prescription_screen.dart';
import '../../features/patient_records/data/models/prescription_model.dart';
import '../../features/patient_records/presentation/pages/note_detail_screen.dart';
import '../../features/auth/presentation/pages/hospital_admin_screen.dart';

final goRouterProvider = Provider<GoRouter>((ref) {
  // Notifier to trigger GoRouter redirects when auth state changes
  final authNotifier = ValueNotifier(ref.read(authControllerProvider));
  
  ref.listen(authControllerProvider, (_, next) {
    authNotifier.value = next;
  });

  return GoRouter(
    initialLocation: '/',
    refreshListenable: authNotifier,
    redirect: (context, state) {
      final authState = authNotifier.value;
      final isAuth = authState.value != null;
      final isGoingToLogin = state.matchedLocation == '/login' || state.matchedLocation == '/role_selection';
      
      // If the app is starting up or processing auth, stay where we are
      if (authState.isLoading) return null;

      // Protect all routes except splash, login, and role selection
      if (!isAuth && !isGoingToLogin && state.matchedLocation != '/') {
        return '/role_selection';
      }

      // If authenticated and trying to go to login, redirect to dashboard
      if (isAuth && isGoingToLogin) {
        return '/dashboard';
      }

      return null;
    },
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
        path: '/medical_records',
        builder: (context, state) => const MedicalRecordsScreen(),
      ),
      GoRoute(
        path: '/add_clinical_note',
        builder: (context, state) => const AddClinicalNoteScreen(),
      ),
      GoRoute(
        path: '/voice_dictation',
        builder: (context, state) => const VoiceDictationScreen(),
      ),
      GoRoute(
        path: '/ai_categorization',
        builder: (context, state) => const AiCategorizationScreen(),
      ),
      GoRoute(
        path: '/capture',
        builder: (context, state) => const CaptureScreen(),
      ),
      GoRoute(
        path: '/upload_confirmation',
        builder: (context, state) => const UploadConfirmationScreen(),
      ),
      GoRoute(
        path: '/ai_scan_result',
        builder: (context, state) {
          final autoLaunch = state.extra == true;
          return AiScanResultScreen(autoLaunchCamera: autoLaunch);
        },
      ),
      GoRoute(
        path: '/ai_categorization_result',
        builder: (context, state) => const AiCategorizationResultScreen(),
      ),
      GoRoute(
        path: '/clinical_notes',
        builder: (context, state) => const ClinicalNotesScreen(),
      ),
      GoRoute(
        path: '/prescriptions',
        builder: (context, state) => const PrescriptionsScreen(),
      ),
      GoRoute(
        path: '/add_prescription',
        builder: (context, state) {
          // If extras carry a PrescriptionModel, open in edit mode
          final prescription = state.extra is PrescriptionModel
              ? state.extra as PrescriptionModel
              : null;
          return AddPrescriptionScreen(prescription: prescription);
        },
      ),
      GoRoute(
        path: '/note_detail',
        builder: (context, state) => const NoteDetailScreen(),
      ),
      GoRoute(
        path: '/hospital_admin',
        builder: (context, state) => const HospitalAdminScreen(),
      ),
    ],
  );
});
