// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'patient_models.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$Patient {

 String get id; String? get firstName; String? get lastName; String? get middleName; String? get dateOfBirth; String? get gender; String? get bloodGroup; String? get maritalStatus; String? get phone; String? get email; String? get address; String? get emergencyContactName; String? get emergencyContactPhone; String? get profileImageUrl; Map<String, dynamic>? get fhirMetadata;
/// Create a copy of Patient
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$PatientCopyWith<Patient> get copyWith => _$PatientCopyWithImpl<Patient>(this as Patient, _$identity);

  /// Serializes this Patient to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Patient&&(identical(other.id, id) || other.id == id)&&(identical(other.firstName, firstName) || other.firstName == firstName)&&(identical(other.lastName, lastName) || other.lastName == lastName)&&(identical(other.middleName, middleName) || other.middleName == middleName)&&(identical(other.dateOfBirth, dateOfBirth) || other.dateOfBirth == dateOfBirth)&&(identical(other.gender, gender) || other.gender == gender)&&(identical(other.bloodGroup, bloodGroup) || other.bloodGroup == bloodGroup)&&(identical(other.maritalStatus, maritalStatus) || other.maritalStatus == maritalStatus)&&(identical(other.phone, phone) || other.phone == phone)&&(identical(other.email, email) || other.email == email)&&(identical(other.address, address) || other.address == address)&&(identical(other.emergencyContactName, emergencyContactName) || other.emergencyContactName == emergencyContactName)&&(identical(other.emergencyContactPhone, emergencyContactPhone) || other.emergencyContactPhone == emergencyContactPhone)&&(identical(other.profileImageUrl, profileImageUrl) || other.profileImageUrl == profileImageUrl)&&const DeepCollectionEquality().equals(other.fhirMetadata, fhirMetadata));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,firstName,lastName,middleName,dateOfBirth,gender,bloodGroup,maritalStatus,phone,email,address,emergencyContactName,emergencyContactPhone,profileImageUrl,const DeepCollectionEquality().hash(fhirMetadata));

@override
String toString() {
  return 'Patient(id: $id, firstName: $firstName, lastName: $lastName, middleName: $middleName, dateOfBirth: $dateOfBirth, gender: $gender, bloodGroup: $bloodGroup, maritalStatus: $maritalStatus, phone: $phone, email: $email, address: $address, emergencyContactName: $emergencyContactName, emergencyContactPhone: $emergencyContactPhone, profileImageUrl: $profileImageUrl, fhirMetadata: $fhirMetadata)';
}


}

/// @nodoc
abstract mixin class $PatientCopyWith<$Res>  {
  factory $PatientCopyWith(Patient value, $Res Function(Patient) _then) = _$PatientCopyWithImpl;
@useResult
$Res call({
 String id, String? firstName, String? lastName, String? middleName, String? dateOfBirth, String? gender, String? bloodGroup, String? maritalStatus, String? phone, String? email, String? address, String? emergencyContactName, String? emergencyContactPhone, String? profileImageUrl, Map<String, dynamic>? fhirMetadata
});




}
/// @nodoc
class _$PatientCopyWithImpl<$Res>
    implements $PatientCopyWith<$Res> {
  _$PatientCopyWithImpl(this._self, this._then);

  final Patient _self;
  final $Res Function(Patient) _then;

/// Create a copy of Patient
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? firstName = freezed,Object? lastName = freezed,Object? middleName = freezed,Object? dateOfBirth = freezed,Object? gender = freezed,Object? bloodGroup = freezed,Object? maritalStatus = freezed,Object? phone = freezed,Object? email = freezed,Object? address = freezed,Object? emergencyContactName = freezed,Object? emergencyContactPhone = freezed,Object? profileImageUrl = freezed,Object? fhirMetadata = freezed,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,firstName: freezed == firstName ? _self.firstName : firstName // ignore: cast_nullable_to_non_nullable
as String?,lastName: freezed == lastName ? _self.lastName : lastName // ignore: cast_nullable_to_non_nullable
as String?,middleName: freezed == middleName ? _self.middleName : middleName // ignore: cast_nullable_to_non_nullable
as String?,dateOfBirth: freezed == dateOfBirth ? _self.dateOfBirth : dateOfBirth // ignore: cast_nullable_to_non_nullable
as String?,gender: freezed == gender ? _self.gender : gender // ignore: cast_nullable_to_non_nullable
as String?,bloodGroup: freezed == bloodGroup ? _self.bloodGroup : bloodGroup // ignore: cast_nullable_to_non_nullable
as String?,maritalStatus: freezed == maritalStatus ? _self.maritalStatus : maritalStatus // ignore: cast_nullable_to_non_nullable
as String?,phone: freezed == phone ? _self.phone : phone // ignore: cast_nullable_to_non_nullable
as String?,email: freezed == email ? _self.email : email // ignore: cast_nullable_to_non_nullable
as String?,address: freezed == address ? _self.address : address // ignore: cast_nullable_to_non_nullable
as String?,emergencyContactName: freezed == emergencyContactName ? _self.emergencyContactName : emergencyContactName // ignore: cast_nullable_to_non_nullable
as String?,emergencyContactPhone: freezed == emergencyContactPhone ? _self.emergencyContactPhone : emergencyContactPhone // ignore: cast_nullable_to_non_nullable
as String?,profileImageUrl: freezed == profileImageUrl ? _self.profileImageUrl : profileImageUrl // ignore: cast_nullable_to_non_nullable
as String?,fhirMetadata: freezed == fhirMetadata ? _self.fhirMetadata : fhirMetadata // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>?,
  ));
}

}


/// Adds pattern-matching-related methods to [Patient].
extension PatientPatterns on Patient {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _Patient value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _Patient() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _Patient value)  $default,){
final _that = this;
switch (_that) {
case _Patient():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _Patient value)?  $default,){
final _that = this;
switch (_that) {
case _Patient() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String? firstName,  String? lastName,  String? middleName,  String? dateOfBirth,  String? gender,  String? bloodGroup,  String? maritalStatus,  String? phone,  String? email,  String? address,  String? emergencyContactName,  String? emergencyContactPhone,  String? profileImageUrl,  Map<String, dynamic>? fhirMetadata)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _Patient() when $default != null:
return $default(_that.id,_that.firstName,_that.lastName,_that.middleName,_that.dateOfBirth,_that.gender,_that.bloodGroup,_that.maritalStatus,_that.phone,_that.email,_that.address,_that.emergencyContactName,_that.emergencyContactPhone,_that.profileImageUrl,_that.fhirMetadata);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String? firstName,  String? lastName,  String? middleName,  String? dateOfBirth,  String? gender,  String? bloodGroup,  String? maritalStatus,  String? phone,  String? email,  String? address,  String? emergencyContactName,  String? emergencyContactPhone,  String? profileImageUrl,  Map<String, dynamic>? fhirMetadata)  $default,) {final _that = this;
switch (_that) {
case _Patient():
return $default(_that.id,_that.firstName,_that.lastName,_that.middleName,_that.dateOfBirth,_that.gender,_that.bloodGroup,_that.maritalStatus,_that.phone,_that.email,_that.address,_that.emergencyContactName,_that.emergencyContactPhone,_that.profileImageUrl,_that.fhirMetadata);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String? firstName,  String? lastName,  String? middleName,  String? dateOfBirth,  String? gender,  String? bloodGroup,  String? maritalStatus,  String? phone,  String? email,  String? address,  String? emergencyContactName,  String? emergencyContactPhone,  String? profileImageUrl,  Map<String, dynamic>? fhirMetadata)?  $default,) {final _that = this;
switch (_that) {
case _Patient() when $default != null:
return $default(_that.id,_that.firstName,_that.lastName,_that.middleName,_that.dateOfBirth,_that.gender,_that.bloodGroup,_that.maritalStatus,_that.phone,_that.email,_that.address,_that.emergencyContactName,_that.emergencyContactPhone,_that.profileImageUrl,_that.fhirMetadata);case _:
  return null;

}
}

}

/// @nodoc

@JsonSerializable(fieldRename: FieldRename.snake)
class _Patient extends Patient {
  const _Patient({required this.id, this.firstName, this.lastName, this.middleName, this.dateOfBirth, this.gender, this.bloodGroup, this.maritalStatus, this.phone, this.email, this.address, this.emergencyContactName, this.emergencyContactPhone, this.profileImageUrl, final  Map<String, dynamic>? fhirMetadata}): _fhirMetadata = fhirMetadata,super._();
  factory _Patient.fromJson(Map<String, dynamic> json) => _$PatientFromJson(json);

@override final  String id;
@override final  String? firstName;
@override final  String? lastName;
@override final  String? middleName;
@override final  String? dateOfBirth;
@override final  String? gender;
@override final  String? bloodGroup;
@override final  String? maritalStatus;
@override final  String? phone;
@override final  String? email;
@override final  String? address;
@override final  String? emergencyContactName;
@override final  String? emergencyContactPhone;
@override final  String? profileImageUrl;
 final  Map<String, dynamic>? _fhirMetadata;
@override Map<String, dynamic>? get fhirMetadata {
  final value = _fhirMetadata;
  if (value == null) return null;
  if (_fhirMetadata is EqualUnmodifiableMapView) return _fhirMetadata;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableMapView(value);
}


/// Create a copy of Patient
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$PatientCopyWith<_Patient> get copyWith => __$PatientCopyWithImpl<_Patient>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$PatientToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _Patient&&(identical(other.id, id) || other.id == id)&&(identical(other.firstName, firstName) || other.firstName == firstName)&&(identical(other.lastName, lastName) || other.lastName == lastName)&&(identical(other.middleName, middleName) || other.middleName == middleName)&&(identical(other.dateOfBirth, dateOfBirth) || other.dateOfBirth == dateOfBirth)&&(identical(other.gender, gender) || other.gender == gender)&&(identical(other.bloodGroup, bloodGroup) || other.bloodGroup == bloodGroup)&&(identical(other.maritalStatus, maritalStatus) || other.maritalStatus == maritalStatus)&&(identical(other.phone, phone) || other.phone == phone)&&(identical(other.email, email) || other.email == email)&&(identical(other.address, address) || other.address == address)&&(identical(other.emergencyContactName, emergencyContactName) || other.emergencyContactName == emergencyContactName)&&(identical(other.emergencyContactPhone, emergencyContactPhone) || other.emergencyContactPhone == emergencyContactPhone)&&(identical(other.profileImageUrl, profileImageUrl) || other.profileImageUrl == profileImageUrl)&&const DeepCollectionEquality().equals(other._fhirMetadata, _fhirMetadata));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,firstName,lastName,middleName,dateOfBirth,gender,bloodGroup,maritalStatus,phone,email,address,emergencyContactName,emergencyContactPhone,profileImageUrl,const DeepCollectionEquality().hash(_fhirMetadata));

@override
String toString() {
  return 'Patient(id: $id, firstName: $firstName, lastName: $lastName, middleName: $middleName, dateOfBirth: $dateOfBirth, gender: $gender, bloodGroup: $bloodGroup, maritalStatus: $maritalStatus, phone: $phone, email: $email, address: $address, emergencyContactName: $emergencyContactName, emergencyContactPhone: $emergencyContactPhone, profileImageUrl: $profileImageUrl, fhirMetadata: $fhirMetadata)';
}


}

/// @nodoc
abstract mixin class _$PatientCopyWith<$Res> implements $PatientCopyWith<$Res> {
  factory _$PatientCopyWith(_Patient value, $Res Function(_Patient) _then) = __$PatientCopyWithImpl;
@override @useResult
$Res call({
 String id, String? firstName, String? lastName, String? middleName, String? dateOfBirth, String? gender, String? bloodGroup, String? maritalStatus, String? phone, String? email, String? address, String? emergencyContactName, String? emergencyContactPhone, String? profileImageUrl, Map<String, dynamic>? fhirMetadata
});




}
/// @nodoc
class __$PatientCopyWithImpl<$Res>
    implements _$PatientCopyWith<$Res> {
  __$PatientCopyWithImpl(this._self, this._then);

  final _Patient _self;
  final $Res Function(_Patient) _then;

/// Create a copy of Patient
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? firstName = freezed,Object? lastName = freezed,Object? middleName = freezed,Object? dateOfBirth = freezed,Object? gender = freezed,Object? bloodGroup = freezed,Object? maritalStatus = freezed,Object? phone = freezed,Object? email = freezed,Object? address = freezed,Object? emergencyContactName = freezed,Object? emergencyContactPhone = freezed,Object? profileImageUrl = freezed,Object? fhirMetadata = freezed,}) {
  return _then(_Patient(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,firstName: freezed == firstName ? _self.firstName : firstName // ignore: cast_nullable_to_non_nullable
as String?,lastName: freezed == lastName ? _self.lastName : lastName // ignore: cast_nullable_to_non_nullable
as String?,middleName: freezed == middleName ? _self.middleName : middleName // ignore: cast_nullable_to_non_nullable
as String?,dateOfBirth: freezed == dateOfBirth ? _self.dateOfBirth : dateOfBirth // ignore: cast_nullable_to_non_nullable
as String?,gender: freezed == gender ? _self.gender : gender // ignore: cast_nullable_to_non_nullable
as String?,bloodGroup: freezed == bloodGroup ? _self.bloodGroup : bloodGroup // ignore: cast_nullable_to_non_nullable
as String?,maritalStatus: freezed == maritalStatus ? _self.maritalStatus : maritalStatus // ignore: cast_nullable_to_non_nullable
as String?,phone: freezed == phone ? _self.phone : phone // ignore: cast_nullable_to_non_nullable
as String?,email: freezed == email ? _self.email : email // ignore: cast_nullable_to_non_nullable
as String?,address: freezed == address ? _self.address : address // ignore: cast_nullable_to_non_nullable
as String?,emergencyContactName: freezed == emergencyContactName ? _self.emergencyContactName : emergencyContactName // ignore: cast_nullable_to_non_nullable
as String?,emergencyContactPhone: freezed == emergencyContactPhone ? _self.emergencyContactPhone : emergencyContactPhone // ignore: cast_nullable_to_non_nullable
as String?,profileImageUrl: freezed == profileImageUrl ? _self.profileImageUrl : profileImageUrl // ignore: cast_nullable_to_non_nullable
as String?,fhirMetadata: freezed == fhirMetadata ? _self._fhirMetadata : fhirMetadata // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>?,
  ));
}


}

// dart format on
