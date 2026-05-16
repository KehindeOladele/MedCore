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
      final repo = ref.read(authRepositoryProvider);
      final storage = ref.read(secureStorageServiceProvider);

      // 1. Register the user via POST /auth/signup
      await repo.signup(SignupRequest(email: email, password: password));

      // 2. Immediately log in with the same credentials to get a real token.
      //    The signup endpoint only returns {id, email, role} — no token.
      final token = await repo.login(LoginRequest(email: email, password: password));

      // 3. Persist the token for all future authenticated requests
      await storage.saveToken(token);

      // 4. Fetch the actual user profile to populate the state
      final user = await repo.getMe();

      state = AsyncData(user);
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
