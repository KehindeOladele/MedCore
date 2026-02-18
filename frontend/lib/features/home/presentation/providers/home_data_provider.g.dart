// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'home_data_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(homeRepository)
final homeRepositoryProvider = HomeRepositoryProvider._();

final class HomeRepositoryProvider
    extends $FunctionalProvider<HomeRepository, HomeRepository, HomeRepository>
    with $Provider<HomeRepository> {
  HomeRepositoryProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'homeRepositoryProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$homeRepositoryHash();

  @$internal
  @override
  $ProviderElement<HomeRepository> $createElement($ProviderPointer pointer) =>
      $ProviderElement(pointer);

  @override
  HomeRepository create(Ref ref) {
    return homeRepository(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(HomeRepository value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<HomeRepository>(value),
    );
  }
}

String _$homeRepositoryHash() => r'a7ad35b71d152c2f2e026facffd4f91979e425ab';

@ProviderFor(vitals)
final vitalsProvider = VitalsProvider._();

final class VitalsProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<VitalModel>>,
          List<VitalModel>,
          FutureOr<List<VitalModel>>
        >
    with $FutureModifier<List<VitalModel>>, $FutureProvider<List<VitalModel>> {
  VitalsProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'vitalsProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$vitalsHash();

  @$internal
  @override
  $FutureProviderElement<List<VitalModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<VitalModel>> create(Ref ref) {
    return vitals(ref);
  }
}

String _$vitalsHash() => r'7ced7b87894ffa20317066d5a300dee78ce33d55';

@ProviderFor(reminders)
final remindersProvider = RemindersProvider._();

final class RemindersProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<ReminderModel>>,
          List<ReminderModel>,
          FutureOr<List<ReminderModel>>
        >
    with
        $FutureModifier<List<ReminderModel>>,
        $FutureProvider<List<ReminderModel>> {
  RemindersProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'remindersProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$remindersHash();

  @$internal
  @override
  $FutureProviderElement<List<ReminderModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<ReminderModel>> create(Ref ref) {
    return reminders(ref);
  }
}

String _$remindersHash() => r'c14fd901febae0744e2434960da73c3eaa16fd94';

@ProviderFor(recentActivity)
final recentActivityProvider = RecentActivityProvider._();

final class RecentActivityProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<ActivityModel>>,
          List<ActivityModel>,
          FutureOr<List<ActivityModel>>
        >
    with
        $FutureModifier<List<ActivityModel>>,
        $FutureProvider<List<ActivityModel>> {
  RecentActivityProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'recentActivityProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$recentActivityHash();

  @$internal
  @override
  $FutureProviderElement<List<ActivityModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<ActivityModel>> create(Ref ref) {
    return recentActivity(ref);
  }
}

String _$recentActivityHash() => r'b2ec4c47ebe6c9e18db773d99970c6b457ea2b3c';

@ProviderFor(prescriptions)
final prescriptionsProvider = PrescriptionsProvider._();

final class PrescriptionsProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<PrescriptionModel>>,
          List<PrescriptionModel>,
          FutureOr<List<PrescriptionModel>>
        >
    with
        $FutureModifier<List<PrescriptionModel>>,
        $FutureProvider<List<PrescriptionModel>> {
  PrescriptionsProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'prescriptionsProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$prescriptionsHash();

  @$internal
  @override
  $FutureProviderElement<List<PrescriptionModel>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<PrescriptionModel>> create(Ref ref) {
    return prescriptions(ref);
  }
}

String _$prescriptionsHash() => r'8717693a2aa71726bea60236ce6abb27e4554a99';
