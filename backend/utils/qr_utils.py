"""Module: utils/qr_utils.py"""
import io

import qrcode


def generate_qr_bytes(data: str) -> bytes:
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


def generate_piece_qr_url(piece_id: str, base_url: str = "") -> str:
    return f"{base_url}/passport/{piece_id}"
