import '../../../../core/services/api_service.dart';
import '../../../../core/services/auth_service.dart';
import '../models/user_summary_model.dart';

class DashboardRepository {
  final ApiService _api;

  DashboardRepository() : _api = ApiService(AuthService.instance);

  /// Calls `GET /api/v1/user/summary` and returns a [UserSummaryModel].
  Future<UserSummaryModel> getUserSummary() async {
    final data = await _api.get('/api/v1/user/summary');
    return UserSummaryModel.fromJson(Map<String, dynamic>.from(data as Map));
  }
}
