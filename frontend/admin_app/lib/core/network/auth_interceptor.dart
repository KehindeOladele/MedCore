import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../storage/secure_storage_service.dart';

part 'auth_interceptor.g.dart';

class AuthInterceptor extends Interceptor {
  final SecureStorageService _storageService;

  AuthInterceptor(this._storageService);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Determine if the route requires a token.
    // By default, we might add it to all requests except auth/login and auth/signup
    final isAuthRoute = options.path.contains('/auth/signup') || 
                        (options.path.contains('/auth/') && !options.path.contains('/auth/me'));
    
    if (!isAuthRoute) {
      final token = await _storageService.getToken();
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }
    
    super.onRequest(options, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // If the server returns a 401 Unauthorized, we might want to trigger a logout
    if (err.response?.statusCode == 401) {
      // Handle logout or token refresh here
    }
    super.onError(err, handler);
  }
}

@riverpod
AuthInterceptor authInterceptor(Ref ref) {
  final storageService = ref.watch(secureStorageServiceProvider);
  return AuthInterceptor(storageService);
}
