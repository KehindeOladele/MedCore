// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'patient_repository.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(patientRepository)
const patientRepositoryProvider = PatientRepositoryProvider._();

final class PatientRepositoryProvider
    extends
        $FunctionalProvider<
          PatientRepository,
          PatientRepository,
          PatientRepository
        >
    with $Provider<PatientRepository> {
  const PatientRepositoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'patientRepositoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$patientRepositoryHash();

  @$internal
  @override
  $ProviderElement<PatientRepository> $createElement(
    $ProviderPointer pointer,
  ) => $ProviderElement(pointer);

  @override
  PatientRepository create(Ref ref) {
    return patientRepository(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(PatientRepository value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<PatientRepository>(value),
    );
  }
}

String _$patientRepositoryHash() => r'68ed3be6a770b441fe6e13bc00eabe7c8b1ce1f6';
