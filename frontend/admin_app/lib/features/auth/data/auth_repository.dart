import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../../core/network/api_client.dart';
import '../../../core/storage/secure_storage_service.dart';
import 'models/auth_models.dart';

part 'auth_repository.g.dart';

class AuthRepository {
  final ApiClient _apiClient;
  final SecureStorageService _storageService;

  AuthRepository(this._apiClient, this._storageService);

  Future<String> login(LoginRequest request) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/login',
        data: request.toJson(),
      );
      // The backend response schema is open ({}), so we extract the token
      // defensively — checking both common field names.
      final data = response.data as Map<String, dynamic>;
      final token = data['access_token'] ?? data['token'] ?? data['accessToken'];
      if (token == null) {
        throw Exception('Login succeeded but no token was returned. Response: $data');
      }
      return token as String;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<SignupResponse> signup(SignupRequest request) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/signup',
        data: request.toJson(),
      );
      return SignupResponse.fromJson(response.data);
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<UserMe> getMe() async {
    try {
      final response = await _apiClient.dio.get('/auth/me');
      return UserMe.fromJson(response.data);
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> logout() async {
    await _storageService.deleteToken();
  }

  Exception _handleError(dynamic error) {
    if (error is DioException) {
      if (error.response != null) {
        return Exception('Server error: ${error.response?.data}');
      }
      return Exception('Network error: ${error.message}');
    }
    return Exception('Unknown error: $error');
  }
}

@riverpod
AuthRepository authRepository(Ref ref) {
  final apiClient = ref.watch(apiClientProvider);
  final storageService = ref.watch(secureStorageServiceProvider);
  return AuthRepository(apiClient, storageService);
}
