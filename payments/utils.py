def calculate_total_amount(
    *,
    base_amount: int,
    channel: dict,
    payment_method: str,
):
    tax_percent = channel.get("tax_percent", 0)

    fee_total = 0

    # 1️⃣ Aggregator fee (VA)
    aggregator_fee = channel.get("aggregator_fee")
    if aggregator_fee:
        if aggregator_fee["type"] == "flat":
            fee_total += aggregator_fee["value"]
        else:
            fee_total += round(base_amount * aggregator_fee["value"] / 100)

    # 2️⃣ Method fee (OPTIONAL)
    method_config = channel["methods"].get(payment_method)
    if not method_config:
        raise ValueError("Invalid payment method")

    fee_config = method_config.get("fee")  # ✅ SAFE
    if fee_config:
        if fee_config["type"] == "flat":
            fee_total += fee_config["value"]
        else:
            fee_total += round(base_amount * fee_config["value"] / 100)

    # 3️⃣ Tax dari TOTAL FEE
    tax = round(fee_total * tax_percent / 100)

    total = base_amount + fee_total + tax

    return {
        "base_amount": base_amount,
        "fee": fee_total,
        "tax": tax,
        "total": total,
    }
