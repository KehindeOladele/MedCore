import 'package:flutter/material.dart';

class PrescriptionModel {
  final String id;
  final String name;
  final String dosage;
  final String frequency;
  final String doctor;
  final String instructions;
  final DateTime? startDate;
  final DateTime? endDate;
  final TimeOfDay reminderTime;
  final bool hasReminder;
  final bool isCompleted;

  PrescriptionModel({
    required this.id,
    required this.name,
    required this.dosage,
    required this.frequency,
    required this.doctor,
    required this.instructions,
    this.startDate,
    this.endDate,
    required this.reminderTime,
    required this.hasReminder,
    this.isCompleted = false,
  });

  String get statusLabel {
    if (isCompleted) return 'Completed';
    // If end date within 7 days, show refill soon
    if (endDate != null && endDate!.difference(DateTime.now()).inDays <= 7) {
      return 'Refill Soon';
    }
    return 'Active';
  }

  String get infoLine {
    if (isCompleted && endDate != null) {
      return 'Finished ${_fmtDate(endDate!)}';
    }
    if (hasReminder) {
      return 'Next dose: ${_formatTime(reminderTime)}';
    }
    return '$dosage • $frequency';
  }

  static String _fmtDate(DateTime d) {
    const months = [
      '',
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ];
    return '${months[d.month]} ${d.day}';
  }

  static String _formatTime(TimeOfDay t) {
    final h = t.hourOfPeriod == 0 ? 12 : t.hourOfPeriod;
    final m = t.minute.toString().padLeft(2, '0');
    final period = t.period == DayPeriod.am ? 'AM' : 'PM';
    return '$h:$m $period';
  }

  PrescriptionModel copyWith({
    String? name,
    String? dosage,
    String? frequency,
    String? doctor,
    String? instructions,
    DateTime? startDate,
    DateTime? endDate,
    TimeOfDay? reminderTime,
    bool? hasReminder,
    bool? isCompleted,
  }) {
    return PrescriptionModel(
      id: id,
      name: name ?? this.name,
      dosage: dosage ?? this.dosage,
      frequency: frequency ?? this.frequency,
      doctor: doctor ?? this.doctor,
      instructions: instructions ?? this.instructions,
      startDate: startDate ?? this.startDate,
      endDate: endDate ?? this.endDate,
      reminderTime: reminderTime ?? this.reminderTime,
      hasReminder: hasReminder ?? this.hasReminder,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}

/// Simple in-memory store using ValueNotifier — no Riverpod/Bloc needed.
class PrescriptionStore {
  PrescriptionStore._();
  static final PrescriptionStore instance = PrescriptionStore._();

  final ValueNotifier<List<PrescriptionModel>> prescriptions = ValueNotifier(
    [],
  );

  void add(PrescriptionModel p) {
    prescriptions.value = [...prescriptions.value, p];
  }

  void update(PrescriptionModel updated) {
    prescriptions.value = [
      for (final p in prescriptions.value)
        if (p.id == updated.id) updated else p,
    ];
  }

  void remove(String id) {
    prescriptions.value = prescriptions.value.where((p) => p.id != id).toList();
  }
}
