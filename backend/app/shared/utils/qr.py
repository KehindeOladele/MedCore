import json
import qrcode
from io import BytesIO


def generate_qr(data: dict):
    payload = json.dumps(data, separators=(",", ":"))
    qr = qrcode.make(payload)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf
