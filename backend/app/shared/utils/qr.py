import json
import qrcode
from io import BytesIO

# ----- QR Code Generation Utility -----
def generate_qr(patient_id: str):
    minimal_payload = {
        "type": "patient",
        "id": patient_id,
        "v": 1
    }

    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # auto
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    # Add the JSON payload to the QR code
    qr.add_data(json.dumps(minimal_payload))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return buf
