import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import '../../../ai_categorization/presentation/pages/ai_categorization_result_screen.dart';

class VoiceDictationScreen extends StatefulWidget {
  const VoiceDictationScreen({super.key});

  @override
  State<VoiceDictationScreen> createState() => _VoiceDictationScreenState();
}

class _VoiceDictationScreenState extends State<VoiceDictationScreen>
    with TickerProviderStateMixin {
  // State
  bool _isRecording = false;
  bool _isDone = false;
  int _elapsedSeconds = 0;
  Timer? _timer;
  final Random _random = Random();

  // Waveform bar heights – animated randomly when recording
  final int _barCount = 28;
  late List<double> _barHeights;

  // Pulse animation
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  // Waveform animation
  late AnimationController _waveController;

  // Simulated transcript lines that appear progressively
  final List<String> _transcriptLines = [
    'Patient presents with recurring acute chest pain—',
    'onset roughly three days ago, rated 6 out of 10.',
    'No radiation to the arm or jaw. Mild dyspnea on exertion.',
    'History of hypertension, currently on Lisinopril 10mg.',
    'Plan: ECG, troponin levels, cardiology referral.',
  ];
  int _visibleLines = 0;
  Timer? _transcriptTimer;

  @override
  void initState() {
    super.initState();
    _barHeights = List.filled(_barCount, 4.0);

    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.18).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    _waveController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 120),
    )..addListener(_updateBars);
  }

  void _updateBars() {
    if (!_isRecording) return;
    setState(() {
      for (int i = 0; i < _barCount; i++) {
        _barHeights[i] = 4.0 + _random.nextDouble() * 44.0;
      }
    });
  }

  void _startRecording() {
    setState(() {
      _isRecording = true;
      _isDone = false;
      _elapsedSeconds = 0;
      _visibleLines = 0;
    });
    _pulseController.repeat(reverse: true);
    _waveController.repeat();

    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() => _elapsedSeconds++);
    });

    // Reveal transcript lines one by one
    _transcriptTimer = Timer.periodic(const Duration(seconds: 3), (_) {
      if (_visibleLines < _transcriptLines.length) {
        setState(() => _visibleLines++);
      } else {
        _transcriptTimer?.cancel();
      }
    });
  }

  void _stopRecording() {
    _timer?.cancel();
    _transcriptTimer?.cancel();
    _waveController.stop();
    _pulseController.stop();
    setState(() {
      _isRecording = false;
      _isDone = true;
      _visibleLines = _transcriptLines.length;
      for (int i = 0; i < _barCount; i++) {
        _barHeights[i] = 4.0;
      }
    });
  }

  void _reRecord() {
    setState(() {
      _isDone = false;
      _elapsedSeconds = 0;
      _visibleLines = 0;
    });
  }

  String _formatTime(int seconds) {
    final m = (seconds ~/ 60).toString().padLeft(2, '0');
    final s = (seconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  @override
  void dispose() {
    _timer?.cancel();
    _transcriptTimer?.cancel();
    _pulseController.dispose();
    _waveController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        scrolledUnderElevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
          onPressed: () => context.pop(),
        ),
        title: Text(
          'Voice Dictation',
          style: TextStyle(
            color: const Color(0xFF0F172A),
            fontSize: 18.sp,
            fontWeight: FontWeight.w700,
            fontFamily: 'Inter',
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 24.h),
                child: Column(
                  children: [
                    // Status label
                    _buildStatusBadge(),
                    SizedBox(height: 32.h),

                    // Mic button with pulse
                    _buildMicButton(),

                    SizedBox(height: 24.h),

                    // Timer display
                    Text(
                      _formatTime(_elapsedSeconds),
                      style: TextStyle(
                        color: _isRecording
                            ? const Color(0xFF059669)
                            : const Color(0xFF94A3B8),
                        fontSize: 40.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                        letterSpacing: 2,
                      ),
                    ),

                    SizedBox(height: 24.h),

                    // Waveform
                    _buildWaveform(),

                    SizedBox(height: 32.h),

                    // Transcript
                    if (_visibleLines > 0) _buildTranscript(),

                    if (!_isRecording && !_isDone) ...[
                      SizedBox(height: 32.h),
                      _buildTipsCard(),
                    ],
                  ],
                ),
              ),
            ),

            // Bottom action buttons
            _buildBottomBar(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusBadge() {
    String label;
    Color bg;
    Color fg;

    if (_isRecording) {
      label = '● Recording...';
      bg = const Color(0xFFDCFCE7);
      fg = const Color(0xFF059669);
    } else if (_isDone) {
      label = '✓ Recording Complete';
      bg = const Color(0xFFDBEAFE);
      fg = const Color(0xFF2563EB);
    } else {
      label = 'Ready to Record';
      bg = const Color(0xFFF1F5F9);
      fg = const Color(0xFF64748B);
    }

    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 8.h),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: fg,
          fontSize: 13.sp,
          fontWeight: FontWeight.w600,
          fontFamily: 'Inter',
        ),
      ),
    );
  }

  Widget _buildMicButton() {
    return GestureDetector(
      onTap: _isDone ? null : (_isRecording ? _stopRecording : _startRecording),
      child: AnimatedBuilder(
        animation: _pulseAnimation,
        builder: (context, child) {
          final scale = _isRecording ? _pulseAnimation.value : 1.0;
          return Transform.scale(scale: scale, child: child);
        },
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Outer ring
            AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              width: 120.w,
              height: 120.w,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _isRecording
                    ? const Color(0xFFEF4444).withValues(alpha: 0.12)
                    : _isDone
                    ? const Color(0xFF059669).withValues(alpha: 0.12)
                    : const Color(0xFF059669).withValues(alpha: 0.08),
              ),
            ),
            // Inner button
            AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              width: 80.w,
              height: 80.w,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _isRecording
                    ? const Color(0xFFEF4444)
                    : const Color(0xFF059669),
                boxShadow: [
                  BoxShadow(
                    color:
                        (_isRecording
                                ? const Color(0xFFEF4444)
                                : const Color(0xFF059669))
                            .withValues(alpha: 0.4),
                    blurRadius: 20,
                    offset: const Offset(0, 6),
                  ),
                ],
              ),
              child: Icon(
                _isDone
                    ? Icons.check
                    : _isRecording
                    ? Icons.stop_rounded
                    : Icons.mic_rounded,
                color: Colors.white,
                size: 34.sp,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWaveform() {
    return SizedBox(
      height: 56.h,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: List.generate(_barCount, (i) {
          return AnimatedContainer(
            duration: const Duration(milliseconds: 80),
            margin: EdgeInsets.symmetric(horizontal: 1.5.w),
            width: 3.w,
            height: _isRecording ? _barHeights[i].h : 4.h,
            decoration: BoxDecoration(
              color: _isRecording
                  ? const Color(
                      0xFF059669,
                    ).withValues(alpha: 0.5 + (_barHeights[i] / 88))
                  : const Color(0xFFE2E8F0),
              borderRadius: BorderRadius.circular(2),
            ),
          );
        }),
      ),
    );
  }

  Widget _buildTranscript() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.text_snippet_outlined,
                color: Color(0xFF64748B),
                size: 16,
              ),
              SizedBox(width: 8.w),
              Text(
                'TRANSCRIPT',
                style: TextStyle(
                  color: const Color(0xFF64748B),
                  fontSize: 11.sp,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.2,
                  fontFamily: 'Inter',
                ),
              ),
            ],
          ),
          SizedBox(height: 12.h),
          ...List.generate(_visibleLines, (i) {
            return AnimatedOpacity(
              duration: const Duration(milliseconds: 400),
              opacity: 1.0,
              child: Padding(
                padding: EdgeInsets.only(bottom: 4.h),
                child: Text(
                  _transcriptLines[i],
                  style: TextStyle(
                    color: const Color(0xFF0F172A),
                    fontSize: 14.sp,
                    height: 1.6,
                    fontFamily: 'Inter',
                  ),
                ),
              ),
            );
          }),
          if (_isRecording) ...[
            SizedBox(height: 4.h),
            // blinking cursor
            _BlinkingCursor(),
          ],
        ],
      ),
    );
  }

  Widget _buildTipsCard() {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(20.w),
      decoration: BoxDecoration(
        color: const Color(0xFFF0FDF4),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFBBF7D0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Tips for best results',
            style: TextStyle(
              color: const Color(0xFF059669),
              fontSize: 13.sp,
              fontWeight: FontWeight.w700,
              fontFamily: 'Inter',
            ),
          ),
          SizedBox(height: 12.h),
          _buildTip('Speak clearly at a moderate pace'),
          _buildTip('Minimize background noise'),
          _buildTip('Hold device 6-12 inches from your mouth'),
        ],
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
            style: TextStyle(
              color: const Color(0xFF059669),
              fontSize: 14.sp,
              fontWeight: FontWeight.bold,
            ),
          ),
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                color: const Color(0xFF475569),
                fontSize: 13.sp,
                fontFamily: 'Inter',
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomBar() {
    return Container(
      padding: EdgeInsets.fromLTRB(24.w, 16.h, 24.w, 32.h),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: _isDone
          ? Row(
              children: [
                // Re-record
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _reRecord,
                    icon: Icon(Icons.refresh, size: 16.sp),
                    label: Text(
                      'Re-record',
                      style: TextStyle(
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w600,
                        fontFamily: 'Inter',
                      ),
                    ),
                    style: OutlinedButton.styleFrom(
                      padding: EdgeInsets.symmetric(vertical: 14.h),
                      foregroundColor: const Color(0xFF475569),
                      side: const BorderSide(color: Color(0xFFE2E8F0)),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 16.w),
                // Confirm
                Expanded(
                  flex: 2,
                  child: ElevatedButton.icon(
                    onPressed: () => Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const AiCategorizationResultScreen(),
                      ),
                    ),
                    icon: Icon(Icons.check_circle_outline, size: 16.sp),
                    label: Text(
                      'Use Transcript',
                      style: TextStyle(
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Inter',
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF059669),
                      foregroundColor: Colors.white,
                      elevation: 0,
                      padding: EdgeInsets.symmetric(vertical: 14.h),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                  ),
                ),
              ],
            )
          : SizedBox(
              width: double.infinity,
              height: 56.h,
              child: ElevatedButton.icon(
                onPressed: _isRecording ? _stopRecording : _startRecording,
                icon: Icon(
                  _isRecording ? Icons.stop_circle_outlined : Icons.mic,
                  size: 20.sp,
                ),
                label: Text(
                  _isRecording ? 'Stop Recording' : 'Start Recording',
                  style: TextStyle(
                    fontSize: 16.sp,
                    fontWeight: FontWeight.w700,
                    fontFamily: 'Inter',
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _isRecording
                      ? const Color(0xFFEF4444)
                      : const Color(0xFF059669),
                  foregroundColor: Colors.white,
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(28),
                  ),
                ),
              ),
            ),
    );
  }
}

// Blinking cursor widget
class _BlinkingCursor extends StatefulWidget {
  @override
  State<_BlinkingCursor> createState() => _BlinkingCursorState();
}

class _BlinkingCursorState extends State<_BlinkingCursor>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    )..repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (_, __) => Opacity(
        opacity: _controller.value,
        child: Container(width: 2, height: 18, color: const Color(0xFF059669)),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
