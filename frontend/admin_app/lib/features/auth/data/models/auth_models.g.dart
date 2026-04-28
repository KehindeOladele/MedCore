// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'auth_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_SignupRequest _$SignupRequestFromJson(Map<String, dynamic> json) =>
    _SignupRequest(
      email: json['email'] as String,
      password: json['password'] as String,
    );

Map<String, dynamic> _$SignupRequestToJson(_SignupRequest instance) =>
    <String, dynamic>{'email': instance.email, 'password': instance.password};

_SignupResponse _$SignupResponseFromJson(Map<String, dynamic> json) =>
    _SignupResponse(
      id: json['id'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
    );

Map<String, dynamic> _$SignupResponseToJson(_SignupResponse instance) =>
    <String, dynamic>{
      'id': instance.id,
      'email': instance.email,
      'role': instance.role,
    };

_UserMe _$UserMeFromJson(Map<String, dynamic> json) => _UserMe(
  id: json['id'] as String,
  email: json['email'] as String,
  role: json['role'] as String,
);

Map<String, dynamic> _$UserMeToJson(_UserMe instance) => <String, dynamic>{
  'id': instance.id,
  'email': instance.email,
  'role': instance.role,
};
