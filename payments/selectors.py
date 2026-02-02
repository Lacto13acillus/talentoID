from .constants import PAYMENT_CHANNELS


def get_payment_channel(code: str):
    for channel in PAYMENT_CHANNELS:
        if channel["code"] == code:
            return channel
    return None
