from copy import deepcopy


_PATIENT = {
    "id": "patient_1",
    "medical_id": "med_1",
    "first_name": "Israel",
    "last_name": "Ayomide",
    "middle_name": "",
    "date_of_birth": "2003 July 12",
    "gender": "Male",
    "blood_group": "AB+",
    "marital_status": "Single",
    "phone": "0803*******",
    "email": "ayomideisrael@gmail.com",
    "address": "Obajana, Kogi state",
    "emergency_contact_name": "Ozioma Micah",
    "emergency_contact_phone": "0708*******",
    "profile_image_url": "https://IsraelAyo.jpeg",
    "fhir_metadata": {
        "id": "patient_1",
        "medical_id": "med_1",
        "first_name": "Israel",
        "last_name": "Ayomide",
        "middle_name": "",
        "date_of_birth": "2003 July 12",
        "gender": "Male",
        "blood_group": "AB+",
        "marital_status": "Single",
        "phone": "0803*******",
        "email": "ayomideisrael@gmail.com",
        "address": "Obajana, Kogi state",
        "emergency_contact_name": "Ozioma Micah",
        "emergency_contact_phone": "0708*******",
        "profile_image_url": "https://IsraelAyo.jpeg",
    }
}


def patient_factory(**overrides):
    patient = deepcopy(_PATIENT)
    patient.update(overrides)
    return patient