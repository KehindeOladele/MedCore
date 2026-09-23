// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'menstrual_cycle_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(menstrualCycleRepository)
final menstrualCycleRepositoryProvider = MenstrualCycleRepositoryProvider._();

final class MenstrualCycleRepositoryProvider
    extends
        $FunctionalProvider<
          MenstrualCycleRepository,
          MenstrualCycleRepository,
          MenstrualCycleRepository
        >
    with $Provider<MenstrualCycleRepository> {
  MenstrualCycleRepositoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'menstrualCycleRepositoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$menstrualCycleRepositoryHash();

  @$internal
  @override
  $ProviderElement<MenstrualCycleRepository> $createElement(
    $ProviderPointer pointer,
  ) => $ProviderElement(pointer);

  @override
  MenstrualCycleRepository create(Ref ref) {
    return menstrualCycleRepository(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(MenstrualCycleRepository value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<MenstrualCycleRepository>(value),
    );
  }
}

String _$menstrualCycleRepositoryHash() =>
    r'cd63cedcc34b3b7043238e76f8559469a3f465b4';

@ProviderFor(MenstrualCycle)
final menstrualCycleProvider = MenstrualCycleProvider._();

final class MenstrualCycleProvider
    extends $AsyncNotifierProvider<MenstrualCycle, MenstrualCycleModel?> {
  MenstrualCycleProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'menstrualCycleProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$menstrualCycleHash();

  @$internal
  @override
  MenstrualCycle create() => MenstrualCycle();
}

String _$menstrualCycleHash() => r'8a26ce721999cfe16a194faa7329b160be8c54e3';

abstract class _$MenstrualCycle extends $AsyncNotifier<MenstrualCycleModel?> {
  FutureOr<MenstrualCycleModel?> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final ref =
        this.ref
            as $Ref<AsyncValue<MenstrualCycleModel?>, MenstrualCycleModel?>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<
                AsyncValue<MenstrualCycleModel?>,
                MenstrualCycleModel?
              >,
              AsyncValue<MenstrualCycleModel?>,
              Object?,
              Object?
            >;
    element.handleCreate(ref, build);
  }
}
