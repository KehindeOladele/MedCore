import 'package:freezed_annotation/freezed_annotation.dart';

part 'auth_models.freezed.dart';
part 'auth_models.g.dart';

@freezed
abstract class LoginRequest with _$LoginRequest {
  const factory LoginRequest({
    required String email,
    required String password,
  }) = _LoginRequest;

  factory LoginRequest.fromJson(Map<String, dynamic> json) =>
      _$LoginRequestFromJson(json);
}

@freezed
abstract class SignupRequest with _$SignupRequest {
  const factory SignupRequest({
    required String email,
    required String password,
  }) = _SignupRequest;

  factory SignupRequest.fromJson(Map<String, dynamic> json) =>
      _$SignupRequestFromJson(json);
}

@freezed
abstract class SignupResponse with _$SignupResponse {
  const factory SignupResponse({
    required String id,
    required String email,
    required String role,
  }) = _SignupResponse;

  factory SignupResponse.fromJson(Map<String, dynamic> json) =>
      _$SignupResponseFromJson(json);
}

@freezed
abstract class UserMe with _$UserMe {
  const factory UserMe({
    required String id,
    required String email,
    required String role,
  }) = _UserMe;

  factory UserMe.fromJson(Map<String, dynamic> json) => _$UserMeFromJson(json);
}
