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
    r'b6c54a553803ebede152f3ec1f894b67f1f0dc29';

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
    r'17c0c9894ec4adf2c6835c5015a4f01c65a69b0a';
