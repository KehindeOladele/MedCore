


# ----- Patient Bundle Builder -----
# def build_patient_bundle(patient, records):
#     return {
#         "resourceType": "Bundle",
#         "type": "collection",
#         "entry": [
#             {"resource": patient},
#             *({"resource": r["clinical_data"]} for r in records)
#         ]
#     }


def build_patient_bundle(patient, records):
    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": patient["id"],
                    **patient.get("fhir_metadata", {})
                }
            },
            *({"resource": r["clinical_data"]} for r in records)
        ]
    }
    