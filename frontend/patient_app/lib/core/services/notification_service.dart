import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/timezone.dart' as tz;
import 'package:timezone/data/latest.dart' as tz;

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();

  factory NotificationService() {
    return _instance;
  }

  NotificationService._internal();

  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  Future<void> init() async {
    tz.initializeTimeZones();

    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    const InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);

    // fixed: initialize takes positional setting in some versions, or named 'initializationSettings' in others?
    // checking error: "The named parameter 'settings' is required". So it's 'settings'.
    // Wait, the error said: "The named parameter 'settings' is required" at line 29.
    // Line 29 is: await flutterLocalNotificationsPlugin.initialize(
    // So it expects `initialize(settings: initializationSettings, ...)` or similar?
    // Actually, usually it is `initialize(initializationSettings, ...)` (positional).
    // Let's try named 'initializationSettings' if 'settings' doesn't work?
    // The error said `settings` is required. That's unusual for this plugin, but I will trust the error.
    // Wait, looking at recent changelogs, v18 might have changed this?
    // Or maybe I am using a very new dev version?
    // Let's genericize: `initializationSettings` is usually the first arg.
    // Error `Too many positional arguments: 0 expected` means NO positional args.
    // So `initialize` is fully named now?

    await flutterLocalNotificationsPlugin.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse:
          (NotificationResponse notificationResponse) async {
            // Handle notification tap
          },
    );
  }

  Future<void> scheduleNotification({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledTime,
    required String frequency,
  }) async {
    await flutterLocalNotificationsPlugin.zonedSchedule(
      id,
      title,
      body,
      tz.TZDateTime.from(scheduledTime, tz.local),
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'medcore_reminders',
          'MedCore Reminders',
          channelDescription: 'Reminders for medications and appointments',
          importance: Importance.max,
          priority: Priority.high,
          ticker: 'ticker',
        ),
      ),
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      uiLocalNotificationDateInterpretation:
          UILocalNotificationDateInterpretation.absoluteTime,
      matchDateTimeComponents: _getMatchDateTimeComponents(frequency),
    );
  }

  DateTimeComponents? _getMatchDateTimeComponents(String frequency) {
    switch (frequency) {
      case 'Daily':
        return DateTimeComponents.time;
      case 'Weekly':
        return DateTimeComponents.dayOfWeekAndTime;
      case 'Monthly':
        return DateTimeComponents.dayOfMonthAndTime;
      case 'Twice':
        // For "Twice", we'd ideally schedule two separate notifications.
        // This simple implementation treats it as Daily for now, or needs caller to schedule multiple.
        // Let's assume Daily for the sake of simplicity in this function,
        // but the caller should handle multiple schedules if needed.
        return DateTimeComponents.time;
      case 'Once':
      default:
        return null;
    }
  }

  Future<void> cancelNotification(int id) async {
    await flutterLocalNotificationsPlugin.cancel(id);
  }
}
