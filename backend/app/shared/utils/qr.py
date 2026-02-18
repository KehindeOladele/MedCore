import json
import qrcode
from io import BytesIO

# ----- QR Code Generation Utility -----
def generate_qr(data: dict):
    minimal_payload = {
        "type": "patient",
        "id": patient_id,
        "v": 1
    }
    qr = qrcode.add_data(json.dumps(minimal_payload))
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf
