import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../../core/network/api_client.dart';
import '../models/patient_models.dart';

part 'patient_repository.g.dart';

@riverpod
PatientRepository patientRepository(Ref ref) {
  return PatientRepository(ref.watch(apiClientProvider));
}

class PatientRepository {
  final ApiClient _apiClient;

  PatientRepository(this._apiClient);

  Future<List<Patient>> getMyPatients() async {
    final response = await _apiClient.dio.get('/patients/mine');
    
    // The swagger endpoint returns a 200 list of objects
    if (response.data is List) {
      return (response.data as List).map((json) => Patient.fromJson(json as Map<String, dynamic>)).toList();
    }
    
    // Fallback if the backend wraps it in a data field
    if (response.data is Map && response.data.containsKey('data')) {
      final dataList = response.data['data'] as List;
      return dataList.map((json) => Patient.fromJson(json as Map<String, dynamic>)).toList();
    }

    throw Exception('Unexpected response format for patients list');
  }
}
