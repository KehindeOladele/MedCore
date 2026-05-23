import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'auth_service.dart';

final apiServiceProvider = Provider<ApiService>((ref) {
  return ApiService(AuthService.instance);
});

class ApiException implements Exception {
  final int statusCode;
  final String message;
  const ApiException({required this.statusCode, required this.message});

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiService {
  // ── Change this to your backend URL ──────────────────────────────────────
  // Use http://10.0.2.2:8000 for Android emulator
  // Use http://localhost:8000 for iOS simulator / Web
  // Use https://medcore-api.onrender.com for production
  static const String _baseUrl = 'https://medcore-0qgd.onrender.com';
  // ─────────────────────────────────────────────────────────────────────────

  final AuthService _authService;

  ApiService(this._authService);

  Future<Map<String, String>> _headers({bool requiresAuth = true}) async {
    final headers = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (requiresAuth) {
      final token = await _authService.getToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }
    return headers;
  }

  dynamic _decode(http.Response response) {
    final body = utf8.decode(response.bodyBytes);
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(body);
    }

    String message;
    try {
      final json = jsonDecode(body);
      message = json['detail'] ?? json['message'] ?? 'Unknown error';
    } catch (_) {
      message = body.isNotEmpty ? body : 'Request failed';
    }

    throw ApiException(statusCode: response.statusCode, message: message);
  }

  Future<dynamic> get(String path, {bool requiresAuth = true}) async {
    final response = await http
        .get(
          Uri.parse('$_baseUrl$path'),
          headers: await _headers(requiresAuth: requiresAuth),
        )
        .timeout(
          const Duration(seconds: 60),
          onTimeout: () {
            throw const ApiException(
              statusCode: 408,
              message: 'Connection timed out',
            );
          },
        );
    return _decode(response);
  }

  Future<dynamic> post(
    String path,
    Map<String, dynamic> body, {
    bool requiresAuth = false,
  }) async {
    final response = await http
        .post(
          Uri.parse('$_baseUrl$path'),
          headers: await _headers(requiresAuth: requiresAuth),
          body: jsonEncode(body),
        )
        .timeout(
          const Duration(seconds: 60),
          onTimeout: () {
            throw const ApiException(
              statusCode: 408,
              message: 'Connection timed out',
            );
          },
        );
    return _decode(response);
  }

  Future<dynamic> put(
    String path,
    Map<String, dynamic> body, {
    bool requiresAuth = true,
  }) async {
    final response = await http
        .put(
          Uri.parse('$_baseUrl$path'),
          headers: await _headers(requiresAuth: requiresAuth),
          body: jsonEncode(body),
        )
        .timeout(
          const Duration(seconds: 60),
          onTimeout: () {
            throw const ApiException(
              statusCode: 408,
              message: 'Connection timed out',
            );
          },
        );
    return _decode(response);
  }
}
