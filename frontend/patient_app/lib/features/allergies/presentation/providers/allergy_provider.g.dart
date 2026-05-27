// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'allergy_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(allergyRepository)
final allergyRepositoryProvider = AllergyRepositoryProvider._();

final class AllergyRepositoryProvider
    extends
        $FunctionalProvider<
          AllergyRepository,
          AllergyRepository,
          AllergyRepository
        >
    with $Provider<AllergyRepository> {
  AllergyRepositoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'allergyRepositoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$allergyRepositoryHash();

  @$internal
  @override
  $ProviderElement<AllergyRepository> $createElement(
    $ProviderPointer pointer,
  ) => $ProviderElement(pointer);

  @override
  AllergyRepository create(Ref ref) {
    return allergyRepository(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(AllergyRepository value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<AllergyRepository>(value),
    );
  }
}

String _$allergyRepositoryHash() => r'8422d2a8f8fdfcef66113e4b26d8b185156b40b4';

@ProviderFor(allergies)
final allergiesProvider = AllergiesProvider._();

final class AllergiesProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<AllergyModel>>,
          List<AllergyModel>,
          FutureOr<List<AllergyModel>>
        >
    with
        $FutureModifier<List<AllergyModel>>,
        $FutureProvider<List<AllergyModel>> {
  AllergiesProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'allergiesProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$allergiesHash();

  @$internal
  @override
  $FutureProviderElement<List<AllergyModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<AllergyModel>> create(Ref ref) {
    return allergies(ref);
  }
}

String _$allergiesHash() => r'2cb095bf7d478cba7e3c6be2eaf7556f31dae7bf';
