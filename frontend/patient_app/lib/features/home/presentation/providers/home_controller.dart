import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'home_controller.g.dart';

@riverpod
class HomeIndex extends _$HomeIndex {
  @override
  int build() {
    return 0;
  }

  void setIndex(int index) {
    state = index;
  }
}

@Riverpod(keepAlive: true)
class GenderNotifier extends _$GenderNotifier {
  @override
  bool build() {
    return true; // Default to female for testing as per request
  }

  void toggleGender() {
    state = !state;
  }

  void setGender(bool isFemale) {
    state = isFemale;
  }
}
