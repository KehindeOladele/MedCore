import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:go_router/go_router.dart';

class RoleSelectionScreen extends StatelessWidget {
  const RoleSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    const Color textDark = Color(0xFF0F172A);
    const Color textGray = Color(0xFF334155);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),

              // Logo Symbol
              Container(
                width: 84,
                height: 86,
                decoration: BoxDecoration(
                  color: const Color.fromRGBO(19, 236, 91, 0.1),
                  borderRadius: BorderRadius.circular(24),
                ),
                child: Center(
                  child: SvgPicture.asset(
                    'assets/icons/medical_cross.svg',
                    width: 38,
                    height: 38,
                    // If the icon needs to be green:
                    // colorFilter: const ColorFilter.mode(Color(0xFF32D74B), BlendMode.srcIn),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // App Title
              const Text(
                'MedCore Admin',
                style: TextStyle(
                  color: textDark,
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                  letterSpacing: -0.6,
                ),
              ),
              const SizedBox(height: 8),

              // Subtitle
              const Text(
                'Select your staff role to continue',
                style: TextStyle(
                  color: textGray,
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),

              const SizedBox(height: 48),

              // Grid of Roles
              Row(
                children: [
                  Expanded(
                    child: _RoleCard(
                      iconPath:
                          'assets/icons/Vector.svg', // fallback icon for Doctor
                      title: 'Doctor',
                      onTap: () => context.push('/login'),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: _RoleCard(
                      iconPath:
                          'assets/icons/nurse.svg', // fallback icon for Nurse
                      title: 'Nurse',
                      onTap: () => context.push('/login'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _RoleCard(
                      iconPath:
                          'assets/icons/penici.svg', // fallback icon for Pharmacist
                      title: 'Pharmacist',
                      onTap: () => context.push('/login'),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: _RoleCard(
                      iconPath:
                          'assets/icons/lab_test.svg', // fallback icon for Lab
                      title: 'Laboratory\nScientist',
                      onTap: () => context.push('/login'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              _RoleCard(
                iconPath: 'assets/icons/admin.svg', // fallback icon for Admin
                title: 'Hospital Administrator',
                isFullWidth: true,
                onTap: () => context.push('/login'),
              ),

              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}

class _RoleCard extends StatelessWidget {
  final String iconPath;
  final String title;
  final VoidCallback onTap;
  final bool isFullWidth;

  const _RoleCard({
    required this.iconPath,
    required this.title,
    required this.onTap,
    this.isFullWidth = false,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 342,
        height: 142,
        decoration: BoxDecoration(
          color: Colors.white, // Standard white background
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: const Color(0xFFF1F5F9)),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.04),
              blurRadius: 25,
              offset: const Offset(0, 10),
            ),
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.04),
              blurRadius: 10,
              offset: const Offset(0, 8),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: const BoxDecoration(
                color: Color(0xFFF8FAFC),
                shape: BoxShape.circle,
              ),
              child: Center(
                child: iconPath.endsWith('.svg')
                    ? SvgPicture.asset(
                        iconPath,
                        width: 24,
                        height: 24,
                        colorFilter: const ColorFilter.mode(
                          Color(0xFF334155),
                          BlendMode.srcIn,
                        ),
                      )
                    : Image.asset(
                        iconPath,
                        width: 24,
                        height: 24,
                        color: const Color(0xFF334155),
                      ),
              ),
            ),
            const SizedBox(height: 16),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Color(0xFF334155),
                fontSize: 14,
                fontWeight: FontWeight.w600,
                height: 1.4,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
