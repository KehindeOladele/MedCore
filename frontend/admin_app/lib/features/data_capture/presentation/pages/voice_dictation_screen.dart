import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

class VoiceDictationScreen extends StatefulWidget {
  const VoiceDictationScreen({super.key});

  @override
  State<VoiceDictationScreen> createState() => _VoiceDictationScreenState();
}

class _VoiceDictationScreenState extends State<VoiceDictationScreen> {
  bool _isRecording = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Record Medical Note'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 20.h),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                'Tap the microphone to start recording',
                style: AppTextStyles.bodyMedium,
              ),
              SizedBox(height: 48.h),
              // Duration counter
              Container(
                padding: EdgeInsets.symmetric(vertical: 24.h, horizontal: 48.w),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  children: [
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.timer_outlined,
                          color: AppColors.textSecondary,
                          size: 20.w,
                        ),
                        SizedBox(width: 8.w),
                        Text('Duration', style: AppTextStyles.bodyMedium),
                      ],
                    ),
                    SizedBox(height: 16.h),
                    Text(
                      _isRecording ? '01:42' : '00:00',
                      style: AppTextStyles.heading1.copyWith(
                        fontSize: 48.sp,
                        color: AppColors.primary,
                      ),
                    ),
                    SizedBox(height: 24.h),
                    // Visualizer wave mock
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: List.generate(15, (index) {
                        return Container(
                          margin: EdgeInsets.symmetric(horizontal: 2.w),
                          width: 4.w,
                          height: _isRecording
                              ? (20 + (index % 5) * 10).h
                              : 4.h,
                          decoration: BoxDecoration(
                            color: _isRecording
                                ? AppColors.secondary
                                : AppColors.border,
                            borderRadius: BorderRadius.circular(2),
                          ),
                        );
                      }),
                    ),
                    SizedBox(height: 32.h),
                    // Record Button
                    GestureDetector(
                      onTap: () {
                        setState(() {
                          _isRecording = !_isRecording;
                        });
                      },
                      child: Container(
                        width: 80.w,
                        height: 80.w,
                        decoration: BoxDecoration(
                          color: _isRecording
                              ? AppColors.error.withValues(alpha: 0.1)
                              : AppColors.primary.withValues(alpha: 0.1),
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Container(
                            width: 56.w,
                            height: 56.w,
                            decoration: BoxDecoration(
                              color: _isRecording
                                  ? AppColors.error
                                  : AppColors.primary,
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              _isRecording ? Icons.stop : Icons.mic,
                              color: Colors.white,
                              size: 32.w,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              // Tips Section
              Container(
                padding: EdgeInsets.all(16.w),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Tips for Best Results',
                      style: AppTextStyles.heading3,
                    ),
                    SizedBox(height: 12.h),
                    _buildTip('Speak clearly and at a moderate pace'),
                    _buildTip('Minimize background noise'),
                    _buildTip('Hold device 6-12 inches from your mouth'),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTip(String text) {
    return Padding(
      padding: EdgeInsets.only(bottom: 8.h),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '• ',
            style: AppTextStyles.bodyMedium.copyWith(
              color: AppColors.primary,
              fontWeight: FontWeight.bold,
            ),
          ),
          Expanded(child: Text(text, style: AppTextStyles.bodyMedium)),
        ],
      ),
    );
  }
}
