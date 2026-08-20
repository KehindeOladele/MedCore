// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'patient_controller.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(PatientController)
const patientControllerProvider = PatientControllerProvider._();

final class PatientControllerProvider
    extends $NotifierProvider<PatientController, AsyncValue<List<Patient>?>> {
  const PatientControllerProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'patientControllerProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$patientControllerHash();

  @$internal
  @override
  PatientController create() => PatientController();

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(AsyncValue<List<Patient>?> value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<AsyncValue<List<Patient>?>>(value),
    );
  }
}

String _$patientControllerHash() => r'cd70faeba4a8a220f6f2996e2a43aa4a3d71e19b';

abstract class _$PatientController
    extends $Notifier<AsyncValue<List<Patient>?>> {
  AsyncValue<List<Patient>?> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final created = build();
    final ref =
        this.ref
            as $Ref<AsyncValue<List<Patient>?>, AsyncValue<List<Patient>?>>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<
                AsyncValue<List<Patient>?>,
                AsyncValue<List<Patient>?>
              >,
              AsyncValue<List<Patient>?>,
              Object?,
              Object?
            >;
    element.handleValue(ref, created);
  }
}
