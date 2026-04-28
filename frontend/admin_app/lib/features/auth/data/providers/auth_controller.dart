import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../models/auth_models.dart';
import '../auth_repository.dart';
import '../../../../../core/storage/secure_storage_service.dart';

part 'auth_controller.g.dart';

@riverpod
class AuthController extends _$AuthController {
  @override
  Future<UserMe?> build() async {
    // On app startup, check if we have a token and load the user
    final token = await ref.read(secureStorageServiceProvider).getToken();
    if (token != null && token.isNotEmpty) {
      try {
        return await ref.read(authRepositoryProvider).getMe();
      } catch (e) {
        // Token might be expired or invalid
        await ref.read(secureStorageServiceProvider).deleteToken();
        return null;
      }
    }
    return null;
  }

  Future<void> login(String email, String password) async {
    state = const AsyncLoading();
    try {
      // TODO: Replace this with the actual login API call when the backend provides the endpoint.
      // Currently, the Swagger API docs do not define a /auth/login route that returns a token.
      
      /*
      // Expected Implementation:
      final response = await ref.read(apiClientProvider).dio.post('/auth/login', data: {
        'email': email,
        'password': password,
      });
      final token = response.data['access_token'];
      await ref.read(secureStorageServiceProvider).saveToken(token);
      final user = await ref.read(authRepositoryProvider).getMe();
      state = AsyncData(user);
      */

      // Simulated Implementation for now:
      await Future.delayed(const Duration(seconds: 1)); // Simulate network request
      
      if (email.isEmpty || password.isEmpty) {
        throw Exception("Invalid credentials");
      }
      
      // Simulate saving a dummy token
      await ref.read(secureStorageServiceProvider).saveToken("dummy_jwt_token");
      
      // Set dummy user state
      state = const AsyncData(UserMe(
        id: "12345",
        email: "doctor@medcore.com",
        role: "admin",
      ));
      
    } catch (e, st) {
      state = AsyncError(e, st);
    }
  }

  Future<void> signup(String email, String password) async {
    state = const AsyncLoading();
    try {
      final req = SignupRequest(email: email, password: password);
      final response = await ref.read(authRepositoryProvider).signup(req);
      
      // If backend login is required after signup, do it here. 
      // For now, we will simulate login success after signup.
      state = AsyncData(UserMe(
        id: response.id,
        email: response.email,
        role: response.role,
      ));
    } catch (e, st) {
      state = AsyncError(e, st);
    }
  }

  Future<void> logout() async {
    state = const AsyncLoading();
    await ref.read(authRepositoryProvider).logout();
    state = const AsyncData(null);
  }
}
