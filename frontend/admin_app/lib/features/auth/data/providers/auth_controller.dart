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
      final repo = ref.read(authRepositoryProvider);
      final storage = ref.read(secureStorageServiceProvider);

      // 1. Call POST /auth/login to get the real token
      final token = await repo.login(LoginRequest(email: email, password: password));

      // 2. Persist the token so ApiClient's interceptor can attach it to all future requests
      await storage.saveToken(token);

      // 3. Fetch the actual logged-in user profile
      final user = await repo.getMe();

      state = AsyncData(user);
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
