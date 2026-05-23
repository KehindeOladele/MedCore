import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/profile_model.dart';
import '../../data/repositories/profile_repository.dart';

final profileProvider = AsyncNotifierProvider<ProfileNotifier, ProfileModel>(() {
  return ProfileNotifier();
});

class ProfileNotifier extends AsyncNotifier<ProfileModel> {
  late ProfileRepository _repository;

  @override
  Future<ProfileModel> build() async {
    _repository = ref.watch(profileRepositoryProvider);
    return _fetchProfile();
  }

  Future<ProfileModel> _fetchProfile() async {
    return await _repository.fetchProfile();
  }

  Future<void> refreshProfile() async {
    state = const AsyncValue.loading();
    try {
      final profile = await _repository.fetchProfile();
      state = AsyncValue.data(profile);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> updateProfile(Map<String, dynamic> payload) async {
    final previousState = state;
    state = const AsyncValue.loading();
    try {
      final updatedProfile = await _repository.updateProfile(payload);
      state = AsyncValue.data(updatedProfile);
    } catch (e, stack) {
      state = previousState; // Revert on failure
      throw e; // Rethrow to let UI handle the error (e.g. Snackbars)
    }
  }
}
