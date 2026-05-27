import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/services/auth_service.dart';
import '../../../../core/services/api_service.dart';

/// Represents the possible states for authentication.
enum AuthStatus { unknown, authenticated, unauthenticated }

class AuthState {
  final AuthStatus status;
  final String? token;
  final String? userId;
  final String? email;
  final String? errorMessage;

  const AuthState({
    this.status = AuthStatus.unknown,
    this.token,
    this.userId,
    this.email,
    this.errorMessage,
  });

  bool get isAuthenticated => status == AuthStatus.authenticated;

  AuthState copyWith({
    AuthStatus? status,
    String? token,
    String? userId,
    String? email,
    String? errorMessage,
  }) {
    return AuthState(
      status: status ?? this.status,
      token: token ?? this.token,
      userId: userId ?? this.userId,
      email: email ?? this.email,
      errorMessage: errorMessage,
    );
  }
}

class AuthNotifier extends AsyncNotifier<AuthState> {
  AuthService get _auth => AuthService.instance;

  @override
  Future<AuthState> build() async {
    // Check for a persisted session on startup
    final hasSession = await _auth.hasSession();
    if (hasSession) {
      final token = await _auth.getToken();
      final userId = await _auth.getUserId();
      final email = await _auth.getUserEmail();
      return AuthState(
        status: AuthStatus.authenticated,
        token: token,
        userId: userId,
        email: email,
      );
    }
    return const AuthState(status: AuthStatus.unauthenticated);
  }

  Future<bool> login(String email, String password) async {
    state = const AsyncValue.loading();
    try {
      await _auth.login(email, password);
      final token = await _auth.getToken();
      final userId = await _auth.getUserId();
      state = AsyncValue.data(
        AuthState(
          status: AuthStatus.authenticated,
          token: token,
          userId: userId,
          email: email,
        ),
      );
      return true;
    } on ApiException catch (e) {
      state = AsyncValue.data(
        AuthState(
          status: AuthStatus.unauthenticated,
          errorMessage: e.message,
        ),
      );
      return false;
    } catch (e) {
      state = AsyncValue.data(
        AuthState(
          status: AuthStatus.unauthenticated,
          errorMessage: 'Network error. Please check your connection.',
        ),
      );
      return false;
    }
  }

  /// Returns the signup status string: 'success' | 'pending_verification'
  Future<String> signup(String email, String password) async {
    state = const AsyncValue.loading();
    try {
      final result = await _auth.signup(email, password);
      final status = result['status'] as String;

      if (status == 'success') {
        // Auto-login after signup if session was created
        final token = await _auth.getToken();
        final userId = await _auth.getUserId();
        state = AsyncValue.data(
          AuthState(
            status: AuthStatus.authenticated,
            token: token,
            userId: userId,
            email: email,
          ),
        );
      } else {
        // pending_verification – keep unauthenticated
        state = const AsyncValue.data(
          AuthState(status: AuthStatus.unauthenticated),
        );
      }
      return status;
    } on ApiException catch (e) {
      state = AsyncValue.data(
        AuthState(
          status: AuthStatus.unauthenticated,
          errorMessage: e.message,
        ),
      );
      rethrow;
    } catch (e) {
      state = AsyncValue.data(
        AuthState(
          status: AuthStatus.unauthenticated,
          errorMessage: 'Network error. Please check your connection.',
        ),
      );
      rethrow;
    }
  }

  Future<void> logout() async {
    await _auth.clearSession();
    state = const AsyncValue.data(
      AuthState(status: AuthStatus.unauthenticated),
    );
  }
}

final authProvider = AsyncNotifierProvider<AuthNotifier, AuthState>(
  AuthNotifier.new,
);
