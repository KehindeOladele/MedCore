import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

const _kTokenKey = 'medcore_access_token';
const _kUserIdKey = 'medcore_user_id';
const _kUserEmailKey = 'medcore_user_email';

class AuthService {
  // ── Singleton so ApiService and providers share one instance ─────────────
  static final AuthService instance = AuthService._();
  AuthService._();

  // ── Token persistence ─────────────────────────────────────────────────────

  Future<void> saveSession({
    required String token,
    required String userId,
    required String email,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kTokenKey, token);
    await prefs.setString(_kUserIdKey, userId);
    await prefs.setString(_kUserEmailKey, email);
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_kTokenKey);
  }

  Future<String?> getUserId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_kUserIdKey);
  }

  Future<String?> getUserEmail() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_kUserEmailKey);
  }

  Future<void> clearSession() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_kTokenKey);
    await prefs.remove(_kUserIdKey);
    await prefs.remove(_kUserEmailKey);
  }

  Future<bool> hasSession() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  // ── API calls (uses a local ApiService instance to avoid circular dep) ────

  late final ApiService _api = ApiService(this);

  /// Returns `{'status': 'success', 'access_token': ..., 'user': {...}}`
  /// or `{'status': 'pending_verification', 'message': ...}`
  Future<Map<String, dynamic>> signup(String email, String password) async {
    final data = await _api.post(
      '/auth/signup',
      {'email': email, 'password': password},
      requiresAuth: false,
    );
    return Map<String, dynamic>.from(data as Map);
  }

  /// Returns the access_token and user info, and persists the session.
  Future<Map<String, dynamic>> login(String email, String password) async {
    final data = await _api.post(
      '/auth/login',
      {'email': email, 'password': password},
      requiresAuth: false,
    );

    final result = Map<String, dynamic>.from(data as Map);
    final token = result['access_token'] as String;
    final user = result['user'] as Map;

    await saveSession(
      token: token,
      userId: user['id'].toString(),
      email: user['email'].toString(),
    );

    return result;
  }
}
