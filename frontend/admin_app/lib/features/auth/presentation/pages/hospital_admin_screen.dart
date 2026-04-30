import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../data/providers/auth_controller.dart';

/// Generic Hospital Admin screen — placeholder until the design team finalises the UI.
/// Allows the super-user (hospital administrator) to test login / signup auth flow
/// and will later host staff registration workflows.
class HospitalAdminScreen extends ConsumerStatefulWidget {
  const HospitalAdminScreen({super.key});

  @override
  ConsumerState<HospitalAdminScreen> createState() =>
      _HospitalAdminScreenState();
}

class _HospitalAdminScreenState extends ConsumerState<HospitalAdminScreen> {
  // --- controllers ---
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;
  bool _isSignUpMode = false; // toggle between Login and Sign Up

  // --- colours (will be replaced by the design system later) ---
  static const Color _green = Color(0xFF059669);
  static const Color _textDark = Color(0xFF0F172A);
  static const Color _textGray = Color(0xFF64748B);
  static const Color _inputBg = Color(0xFFF8FAFC);

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleSubmit() {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill in all fields')),
      );
      return;
    }

    if (_isSignUpMode) {
      ref.read(authControllerProvider.notifier).signup(email, password);
    } else {
      ref.read(authControllerProvider.notifier).login(email, password);
    }
  }

  @override
  Widget build(BuildContext context) {
    ref.listen(authControllerProvider, (previous, next) {
      next.whenOrNull(
        data: (user) {
          if (user != null && previous?.value == null) {
            // Auth success — go to dashboard
            context.go('/dashboard');
          }
        },
        error: (error, _) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                _isSignUpMode
                    ? 'Sign up failed: $error'
                    : 'Login failed: $error',
              ),
              backgroundColor: Colors.red.shade700,
            ),
          );
        },
      );
    });

    final isLoading = ref.watch(authControllerProvider).isLoading;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded,
              color: _textDark, size: 20),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // ── Header ──────────────────────────────────────────
              Container(
                width: 72,
                height: 72,
                decoration: BoxDecoration(
                  color: const Color(0xFFECFDF5),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Center(
                  child: Icon(Icons.admin_panel_settings_rounded,
                      color: _green, size: 36),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Hospital Administration',
                style: TextStyle(
                  color: _textDark,
                  fontSize: 22,
                  fontWeight: FontWeight.w700,
                  letterSpacing: -0.5,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                _isSignUpMode
                    ? 'Create your administrator account'
                    : 'Sign in to manage your hospital',
                style: const TextStyle(
                  color: _textGray,
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),

              // ── Placeholder banner ────────────────────────────
              const SizedBox(height: 24),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFFBEB),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: const Color(0xFFFDE68A)),
                ),
                child: const Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(Icons.construction_rounded,
                        color: Color(0xFFD97706), size: 18),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Design in progress — this screen is a temporary placeholder '
                        'for testing the authentication backend. The final UI will '
                        'be applied once the design team delivers the assets.',
                        style: TextStyle(
                          color: Color(0xFF92400E),
                          fontSize: 12,
                          height: 1.5,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // ── Form card ────────────────────────────────────
              const SizedBox(height: 28),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFFF1F5F9)),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.04),
                      blurRadius: 20,
                      offset: const Offset(0, 6),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Email
                    _label('EMAIL ADDRESS'),
                    const SizedBox(height: 8),
                    _inputField(
                      controller: _emailController,
                      hint: 'admin@hospital.com',
                      keyboardType: TextInputType.emailAddress,
                    ),

                    const SizedBox(height: 20),

                    // Password
                    _label('PASSWORD'),
                    const SizedBox(height: 8),
                    _inputField(
                      controller: _passwordController,
                      hint: '• • • • • • • •',
                      obscure: _obscurePassword,
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off_outlined
                              : Icons.visibility_outlined,
                          color: _textGray,
                          size: 20,
                        ),
                        onPressed: () =>
                            setState(() => _obscurePassword = !_obscurePassword),
                      ),
                    ),

                    const SizedBox(height: 28),

                    // Submit button
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: ElevatedButton(
                        onPressed: isLoading ? null : _handleSubmit,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: _green,
                          foregroundColor: Colors.white,
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        child: isLoading
                            ? const SizedBox(
                                width: 22,
                                height: 22,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2.5,
                                  color: Colors.white,
                                ),
                              )
                            : Text(
                                _isSignUpMode ? 'Create Account' : 'Sign In',
                                style: const TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                      ),
                    ),
                  ],
                ),
              ),

              // ── Toggle login / signup ─────────────────────────
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    _isSignUpMode
                        ? 'Already have an account? '
                        : 'New administrator? ',
                    style: const TextStyle(color: _textGray, fontSize: 13),
                  ),
                  GestureDetector(
                    onTap: () =>
                        setState(() => _isSignUpMode = !_isSignUpMode),
                    child: Text(
                      _isSignUpMode ? 'Sign In' : 'Create Account',
                      style: const TextStyle(
                        color: _green,
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  // ── Helpers ────────────────────────────────────────────────────────────────

  Widget _label(String text) => Text(
        text,
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: _textGray,
          letterSpacing: 0.5,
        ),
      );

  Widget _inputField({
    required TextEditingController controller,
    required String hint,
    TextInputType keyboardType = TextInputType.text,
    bool obscure = false,
    Widget? suffixIcon,
  }) =>
      TextField(
        controller: controller,
        keyboardType: keyboardType,
        obscureText: obscure,
        cursorColor: _green,
        style: const TextStyle(
          fontSize: 15,
          color: _textDark,
          fontWeight: FontWeight.w500,
        ),
        decoration: InputDecoration(
          hintText: hint,
          hintStyle:
              TextStyle(color: _textGray.withValues(alpha: 0.5), fontSize: 15),
          filled: true,
          fillColor: _inputBg,
          suffixIcon: suffixIcon,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: BorderSide.none,
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: _green, width: 2),
          ),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        ),
      );
}
