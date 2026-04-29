// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'auth_controller.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(AuthController)
const authControllerProvider = AuthControllerProvider._();

final class AuthControllerProvider
    extends $AsyncNotifierProvider<AuthController, UserMe?> {
  const AuthControllerProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'authControllerProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$authControllerHash();

  @$internal
  @override
  AuthController create() => AuthController();
}

String _$authControllerHash() => r'de1c26419851faeb483f472f7ff3e82711123b74';

abstract class _$AuthController extends $AsyncNotifier<UserMe?> {
  FutureOr<UserMe?> build();
  @$mustCallSuper
  @override
  void runBuild() {
    final created = build();
    final ref = this.ref as $Ref<AsyncValue<UserMe?>, UserMe?>;
    final element =
        ref.element
            as $ClassProviderElement<
              AnyNotifier<AsyncValue<UserMe?>, UserMe?>,
              AsyncValue<UserMe?>,
              Object?,
              Object?
            >;
    element.handleValue(ref, created);
  }
}
