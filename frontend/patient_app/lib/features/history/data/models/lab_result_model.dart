class LabResultModel {
  final String id;
  final String testName;
  final String status; // 'FINALIZED' | 'PENDING'
  final String? performedDate;
  final String? orderingProvider;
  final String? performingFacility;
  final List<LabResultComponent> results;
  final List<LabAttachment> attachments;

  const LabResultModel({
    required this.id,
    required this.testName,
    required this.status,
    this.performedDate,
    this.orderingProvider,
    this.performingFacility,
    required this.results,
    required this.attachments,
  });

  factory LabResultModel.fromJson(Map<String, dynamic> json) {
    final meta = json['metadata'] as Map<String, dynamic>? ?? {};
    final rawResults = json['results'] as List<dynamic>? ?? [];
    final rawAttachments = json['attachments'] as List<dynamic>? ?? [];

    return LabResultModel(
      id: json['id']?.toString() ?? '',
      testName: json['testName'] as String? ?? 'Lab Test',
      status: json['status'] as String? ?? 'PENDING',
      performedDate: meta['performedDate'] as String?,
      orderingProvider: meta['orderingProvider'] as String?,
      performingFacility: meta['performingFacility'] as String?,
      results: rawResults
          .map((e) => LabResultComponent.fromJson(
                Map<String, dynamic>.from(e as Map),
              ))
          .toList(),
      attachments: rawAttachments
          .map((e) => LabAttachment.fromJson(
                Map<String, dynamic>.from(e as Map),
              ))
          .toList(),
    );
  }
}

class LabResultComponent {
  final String component;
  final num value;
  final String unit;
  final String referenceRange;
  final String flag; // 'Normal' | 'High' | 'Low' | 'Critical'
  final double normalizedScore; // 0.0 – 1.0 for the visual bar

  const LabResultComponent({
    required this.component,
    required this.value,
    required this.unit,
    required this.referenceRange,
    required this.flag,
    required this.normalizedScore,
  });

  factory LabResultComponent.fromJson(Map<String, dynamic> json) {
    return LabResultComponent(
      component: json['component'] as String? ?? 'Unknown',
      value: json['value'] as num? ?? 0,
      unit: json['unit'] as String? ?? '',
      referenceRange: json['referenceRange'] as String? ?? '—',
      flag: json['flag'] as String? ?? 'Normal',
      normalizedScore:
          (json['normalizedScore'] as num?)?.toDouble() ?? 0.5,
    );
  }
}

class LabAttachment {
  final String fileName;
  final String? fileSize;
  final String? url;

  const LabAttachment({
    required this.fileName,
    this.fileSize,
    this.url,
  });

  factory LabAttachment.fromJson(Map<String, dynamic> json) {
    return LabAttachment(
      fileName: json['fileName'] as String? ?? 'attachment',
      fileSize: json['fileSize'] as String?,
      url: json['url'] as String? ?? json['downloadUrl'] as String?,
    );
  }
}
