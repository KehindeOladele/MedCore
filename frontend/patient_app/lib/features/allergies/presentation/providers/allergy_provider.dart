import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/repositories/allergy_repository.dart';
import '../../data/models/allergy_model.dart';

part 'allergy_provider.g.dart';

@riverpod
AllergyRepository allergyRepository(Ref ref) {
  return AllergyRepository();
}

@riverpod
Future<List<AllergyModel>> allergies(Ref ref) async {
  return ref.watch(allergyRepositoryProvider).getAllergies();
}
