import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../../history/data/repositories/lab_repository.dart';
import '../../../history/data/models/lab_result_model.dart';

class LabTestDetailsScreen extends ConsumerWidget {
  /// The lab result ID from the medical history event.
  /// When null the screen shows a "not available" state.
  final String? labId;

  const LabTestDetailsScreen({super.key, this.labId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Lab Test Details',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
            fontSize: 20,
          ),
        ),
        centerTitle: true,
      ),
      body: labId == null
          ? _buildNoId()
          : _buildWithId(context, ref, labId!),
    );
  }

  Widget _buildNoId() {
    return const Center(
      child: Padding(
        padding: EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.science_outlined, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              'No lab result linked to this record.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWithId(BuildContext context, WidgetRef ref, String id) {
    final labAsync = ref.watch(labResultProvider(id));

    return labAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, _) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.orange),
              const SizedBox(height: 16),
              Text(
                'Could not load lab result.\n$err',
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: () => ref.invalidate(labResultProvider(id)),
                icon: const Icon(Icons.refresh),
                label: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      data: (lab) => _buildLabContent(context, lab),
    );
  }

  Widget _buildLabContent(BuildContext context, LabResultModel lab) {
    return Column(
      children: [
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Test Name + Status Badge
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        lab.testName,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF1A1C1E),
                        ),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: lab.status == 'FINALIZED'
                            ? const Color(0xFFE8F5E9)
                            : const Color(0xFFFFF9C4),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        lab.status,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          color: lab.status == 'FINALIZED'
                              ? const Color(0xFF2E7D32)
                              : const Color(0xFFF57F17),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Header Info Card
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.02),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: _buildHeaderItem(
                          icon: Icons.person_outline,
                          label: 'ORDERED BY',
                          value: lab.orderingProvider ?? '—',
                        ),
                      ),
                      Container(
                        width: 1,
                        height: 40,
                        color: Colors.grey[200],
                      ),
                      const SizedBox(width: 24),
                      Expanded(
                        child: _buildHeaderItem(
                          icon: Icons.business_outlined,
                          label: 'FACILITY',
                          value: lab.performingFacility ?? '—',
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),

                // Results Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Results',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1A1C1E),
                      ),
                    ),
                    Text(
                      '${lab.results.length} component${lab.results.length != 1 ? 's' : ''}',
                      style: TextStyle(fontSize: 13, color: Colors.grey[500]),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Result Cards
                if (lab.results.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(24),
                    child: Center(
                      child: Text(
                        'No result components available.',
                        style: TextStyle(color: Colors.grey),
                      ),
                    ),
                  )
                else
                  ...lab.results.map(
                    (component) => LabResultCard(component: component),
                  ),

                // Attachments
                if (lab.attachments.isNotEmpty) ...[
                  const SizedBox(height: 24),
                  const Text(
                    'Attachments',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF1A1C1E),
                    ),
                  ),
                  const SizedBox(height: 12),
                  ...lab.attachments.map(
                    (att) => _buildAttachmentTile(att),
                  ),
                ],
              ],
            ),
          ),
        ),

        // Bottom download button (only if there's at least one attachment)
        if (lab.attachments.isNotEmpty)
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(
                top: BorderSide(color: Colors.grey.withOpacity(0.1)),
              ),
            ),
            child: ElevatedButton.icon(
              onPressed: () async {
                final url = lab.attachments.first.url;
                if (url != null) {
                  final uri = Uri.parse(url);
                  if (await canLaunchUrl(uri)) {
                    await launchUrl(uri,
                        mode: LaunchMode.externalApplication);
                  }
                }
              },
              icon: const Icon(Icons.download_rounded, color: Colors.white),
              label: const Text('Download Official Report'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF009688),
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 56),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                elevation: 0,
                textStyle: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildHeaderItem({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 14, color: const Color(0xFF009688)),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                color: Colors.grey[500],
                letterSpacing: 0.5,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            color: Color(0xFF1A1C1E),
          ),
        ),
      ],
    );
  }

  Widget _buildAttachmentTile(LabAttachment attachment) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.withOpacity(0.15)),
      ),
      child: Row(
        children: [
          const Icon(Icons.picture_as_pdf, color: Color(0xFFE53935), size: 28),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  attachment.fileName,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
                if (attachment.fileSize != null)
                  Text(
                    attachment.fileSize!,
                    style:
                        TextStyle(fontSize: 12, color: Colors.grey[500]),
                  ),
              ],
            ),
          ),
          if (attachment.url != null)
            IconButton(
              icon: const Icon(Icons.open_in_new,
                  color: Color(0xFF009688), size: 20),
              onPressed: () async {
                final uri = Uri.parse(attachment.url!);
                if (await canLaunchUrl(uri)) {
                  await launchUrl(uri,
                      mode: LaunchMode.externalApplication);
                }
              },
            ),
        ],
      ),
    );
  }
}

// ── Result Card ───────────────────────────────────────────────────────────────

enum LabResultStatus { normal, high, low, critical }

class LabResultCard extends StatelessWidget {
  final LabResultComponent component;

  const LabResultCard({super.key, required this.component});

  LabResultStatus get _status {
    switch (component.flag.toLowerCase()) {
      case 'high':
        return LabResultStatus.high;
      case 'low':
        return LabResultStatus.low;
      case 'critical':
        return LabResultStatus.critical;
      default:
        return LabResultStatus.normal;
    }
  }

  @override
  Widget build(BuildContext context) {
    final status = _status;
    final isNormal = status == LabResultStatus.normal;
    final isCritical = status == LabResultStatus.critical;

    final Color statusColor;
    final IconData statusIcon;
    if (isNormal) {
      statusColor = const Color(0xFF00C853);
      statusIcon = Icons.check_circle_outline;
    } else if (isCritical) {
      statusColor = const Color(0xFFD32F2F);
      statusIcon = Icons.warning_rounded;
    } else {
      statusColor = const Color(0xFFFF9800);
      statusIcon = Icons.warning_amber_rounded;
    }

    final statusText = isNormal
        ? 'Normal'
        : isCritical
            ? 'Critical'
            : (status == LabResultStatus.high ? 'High' : 'Low');

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(color: Colors.grey.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                component.component,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1A1C1E),
                ),
              ),
              RichText(
                text: TextSpan(
                  children: [
                    TextSpan(
                      text: component.value.toString(),
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1A1C1E),
                      ),
                    ),
                    TextSpan(
                      text: ' ${component.unit}',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[500],
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Ref: ${component.referenceRange}',
                style: TextStyle(fontSize: 12, color: Colors.grey[500]),
              ),
              Row(
                children: [
                  Icon(statusIcon, size: 14, color: statusColor),
                  const SizedBox(width: 4),
                  Text(
                    statusText,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: statusColor,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 20),
          // Progress Bar
          LayoutBuilder(
            builder: (context, constraints) {
              final width = constraints.maxWidth;
              final progress = component.normalizedScore.clamp(0.0, 1.0);

              return Stack(
                alignment: Alignment.centerLeft,
                children: [
                  // Background track
                  Container(
                    height: 6,
                    width: width,
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
                  // Normal range highlight
                  if (isNormal)
                    Container(
                      height: 6,
                      width: width * 0.6,
                      margin: EdgeInsets.only(left: width * 0.2),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(3),
                      ),
                    )
                  else
                    Container(
                      height: 6,
                      width: width * 0.4,
                      margin: EdgeInsets.only(
                        left: status == LabResultStatus.high
                            ? width * 0.6
                            : 0.0,
                      ),
                      decoration: BoxDecoration(
                        color: statusColor.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(3),
                      ),
                    ),
                  // Marker
                  Container(
                    width: 4,
                    height: 14,
                    margin: EdgeInsets.only(
                      left: (width * progress).clamp(0, width - 4),
                    ),
                    decoration: BoxDecoration(
                      color: isNormal ? Colors.black : statusColor,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}
