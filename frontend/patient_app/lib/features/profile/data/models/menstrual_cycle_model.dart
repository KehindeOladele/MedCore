import 'package:hive/hive.dart';

class MenstrualCycleModel extends HiveObject {
  @HiveField(0)
  DateTime lastPeriodDate;

  @HiveField(1)
  int periodLength;

  @HiveField(2)
  int cycleLength;

  @HiveField(3)
  String flowIntensity;

  MenstrualCycleModel({
    required this.lastPeriodDate,
    required this.periodLength,
    required this.cycleLength,
    required this.flowIntensity,
  });

  // Calculate the predicted start date of the next period
  DateTime get nextPeriodDate =>
      lastPeriodDate.add(Duration(days: cycleLength));

  // Calculate the predicted ovulation date (typically 14 days before next period)
  DateTime get ovulationDate =>
      nextPeriodDate.subtract(const Duration(days: 14));

  // Calculate the fertile window start (5 days before ovulation)
  DateTime get fertileWindowStart =>
      ovulationDate.subtract(const Duration(days: 5));

  // Calculate the fertile window end (1 day after ovulation)
  DateTime get fertileWindowEnd => ovulationDate.add(const Duration(days: 1));
}
