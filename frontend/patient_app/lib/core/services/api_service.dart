import 'dart:convert';
import 'dart:io';
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
  static const String _baseUrl = 'http://10.67.168.224:8000';
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

    // 401 Unauthorized → clear session so the app can redirect to login
    if (response.statusCode == 401) {
      _authService.clearSession();
      throw const ApiException(
        statusCode: 401,
        message: 'Session expired. Please log in again.',
      );
    }

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

  Future<dynamic> postForm(
    String path,
    Map<String, String> body, {
    bool requiresAuth = false,
  }) async {
    final headers = await _headers(requiresAuth: requiresAuth);
    headers['Content-Type'] = 'application/x-www-form-urlencoded';

    final response = await http
        .post(
          Uri.parse('$_baseUrl$path'),
          headers: headers,
          body: body,
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

  Future<dynamic> patch(
    String path,
    Map<String, dynamic> body, {
    bool requiresAuth = true,
  }) async {
    final response = await http
        .patch(
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

  /// Uploads a [file] as multipart/form-data to [path].
  /// [fieldName] defaults to 'file' which matches the FastAPI `File(...)` param name.
  Future<dynamic> postMultipart(
    String path,
    File file, {
    String fieldName = 'file',
    bool requiresAuth = true,
  }) async {
    final token = requiresAuth ? await _authService.getToken() : null;

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$_baseUrl$path'),
    );

    if (token != null) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    request.files.add(
      await http.MultipartFile.fromPath(fieldName, file.path),
    );

    final streamed = await request.send().timeout(
      const Duration(seconds: 120),
      onTimeout: () {
        throw const ApiException(
          statusCode: 408,
          message: 'Upload timed out',
        );
      },
    );

    final response = await http.Response.fromStream(streamed);
    return _decode(response);
  }
}
