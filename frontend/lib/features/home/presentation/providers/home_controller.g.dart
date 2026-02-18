// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'home_controller.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(HomeIndex)
final homeIndexProvider = HomeIndexProvider._();

final class HomeIndexProvider extends $NotifierProvider<HomeIndex, int> {
  HomeIndexProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'homeIndexProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$homeIndexHash();

  @$internal
  @override
  HomeIndex create() => HomeIndex();

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(int value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<int>(value),
    );
  }
}

String _$homeIndexHash() => r'26ce1ffefd5360d1e5cfed9002351f6a1ecee6cb';

abstract class _$HomeIndex extends $Notifier<int> {
  int build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<int, int>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<int, int>,
              int,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}

@ProviderFor(GenderNotifier)
final genderProvider = GenderNotifierProvider._();

final class GenderNotifierProvider
    extends $NotifierProvider<GenderNotifier, bool> {
  GenderNotifierProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'genderProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$genderNotifierHash();

  @$internal
  @override
  GenderNotifier create() => GenderNotifier();

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(bool value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<bool>(value),
    );
  }
}

String _$genderNotifierHash() => r'ccc589fb630444e6c65542a9587cb7184b9abf95';

abstract class _$GenderNotifier extends $Notifier<bool> {
  bool build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref = this.ref as $Ref<bool, bool>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<bool, bool>,
              bool,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}
