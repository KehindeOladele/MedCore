// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'patient_history_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(patientHistoryRepository)
const patientHistoryRepositoryProvider = PatientHistoryRepositoryProvider._();

final class PatientHistoryRepositoryProvider
    extends
        $FunctionalProvider<
          PatientHistoryRepository,
          PatientHistoryRepository,
          PatientHistoryRepository
        >
    with $Provider<PatientHistoryRepository> {
  const PatientHistoryRepositoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'patientHistoryRepositoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$patientHistoryRepositoryHash();

  @$internal
  @override
  $ProviderElement<PatientHistoryRepository> $createElement(
    $ProviderPointer pointer,
  ) => $ProviderElement(pointer);

  @override
  PatientHistoryRepository create(Ref ref) {
    return patientHistoryRepository(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(PatientHistoryRepository value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<PatientHistoryRepository>(value),
    );
  }
}

String _$patientHistoryRepositoryHash() =>
    r'9c6addae52e681f5516d29d9b51e4c94072bae82';

@ProviderFor(patientMedicalHistory)
const patientMedicalHistoryProvider = PatientMedicalHistoryProvider._();

final class PatientMedicalHistoryProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<MedicalHistoryItem>>,
          List<MedicalHistoryItem>,
          FutureOr<List<MedicalHistoryItem>>
        >
    with
        $FutureModifier<List<MedicalHistoryItem>>,
        $FutureProvider<List<MedicalHistoryItem>> {
  const PatientMedicalHistoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'patientMedicalHistoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$patientMedicalHistoryHash();

  @$internal
  @override
  $FutureProviderElement<List<MedicalHistoryItem>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<MedicalHistoryItem>> create(Ref ref) {
    return patientMedicalHistory(ref);
  }
}

String _$patientMedicalHistoryHash() =>
    r'd8503592bc7bc7d42583faabe1252e27f043c0c8';
