import uuid
import requests

from payments.selectors import get_payment_channel
from payments.utils import calculate_total_amount

# yusrandhyy@gmail.com
XENDIT_API_KEY = (
    "xnd_development_21aqQzzUwYgnuftv1UXXqO0qUxaVCndeqoxXC1cPyWcbP9VqKaG8g6vycy6ViM"
)
XENDIT_INVOICE_URL = "https://api.xendit.co/v2/invoices"


def create_registration_invoice(
    *,
    email: str,
    payment_channel_code: str,
    payment_method: str,
    base_amount: int,
):
    # 1️⃣ Validasi channel
    channel = get_payment_channel(payment_channel_code)
    if not channel:
        raise ValueError("Invalid payment channel")

    # 2️⃣ Validasi method milik channel
    allowed_methods = channel.get("methods", [])
    if payment_method not in allowed_methods:
        raise ValueError("Invalid payment method for selected channel")

    # 3️⃣ Hitung fee + tax
    calc = calculate_total_amount(
        base_amount=base_amount,
        channel=channel,
        payment_method=payment_method,
    )

    # 4️⃣ external_id
    external_id = f"register-{uuid.uuid4().hex[:10]}"

    # 5️⃣ Payload ke Xendit (LOCK ke 1 method)
    payload = {
        "external_id": external_id,
        "amount": calc["total"],
        "payer_email": email,
        "description": "Pendaftaran Pemain",
        "payment_methods": [payment_method],  # 👈 satu method terpilih
    }

    # 6️⃣ Call Xendit
    response = requests.post(
        XENDIT_INVOICE_URL,
        auth=(XENDIT_API_KEY, ""),
        json=payload,
        timeout=30,
    )

    print("Xendit response:", response.text)

    response.raise_for_status()
    invoice = response.json()

    return {
        "external_id": external_id,
        "invoice_id": invoice["id"],
        "invoice_url": invoice["invoice_url"],
        "payment_channel": payment_channel_code,
        "payment_method": payment_method,
        "breakdown": calc,
        "amount": calc["total"],
        "expiry_date": invoice["expiry_date"],
    }
