PAYMENT_CHANNELS = [
    {
        "code": "VIRTUAL_ACCOUNT",
        "label": "Virtual Account",
        "aggregator_fee": {
            "type": "flat",
            "value": 4000,
        },
        "tax_percent": 11,
        "methods": {
            "BCA": {"fee": {"type": "flat", "value": 0}},
            "BNI": {"fee": {"type": "flat", "value": 0}},
            "MANDIRI": {"fee": {"type": "flat", "value": 0}},
        },
    },
    {
        "code": "EWALLET",
        "label": "E-Wallet",
        "tax_percent": 11,
        "methods": {
            "OVO": {
                "fee": {"type": "percent", "value": 1.5},
            },
            "JENIUSPAY": {
                "fee": {"type": "percent", "value": 2.0},
            },
            "DANA": {
                "fee": {"type": "percent", "value": 1.5},
            },
            "ASTRAPAY": {
                "fee": {"type": "percent", "value": 1.5},
            },
            "LINKAJA": {
                "fee": {"type": "percent", "value": 1.5},
            },
            "SHOPEEPAY": {
                "fee": {"type": "percent", "value": 2.0},
            },
        },
    },
    {
        "code": "QRIS",
        "label": "QRIS",
        "tax_percent": 11,
        "methods": {
            "QRIS": {
                "fee": {"type": "percent", "value": 0.7},
            }
        },
    },
    {
        "code": "CREDIT_CARD",
        "label": "Kartu Kredit",
        "tax_percent": 11,
        "aggregator_fee": {
            "type": "flat",
            "value": 2000,
        },
        "methods": {
            "CREDIT_CARD": {
                "fee": {"type": "percent", "value": 2.9},
            }
        },
    },
    {
        "code": "OVER_THE_COUNTER",
        "label": "Over the Counter",
        "tax_percent": 11,
        "methods": {
            "ALFAMART": {
                "label": "Alfamart Group",
                "fee": {"type": "flat", "value": 5000},
            },
            "INDOMARET": {
                "label": "Indomaret",
                "fee": {"type": "flat", "value": 5500},
            },
        },
    },
    {
        "code": "PAYLATER",
        "label": "PayLater",
        "tax_percent": 11,
        "methods": {
            "AKULAKU": {
                "label": "Akulaku PayLater",
                "fee": {"type": "percent", "value": 1.7},
            },
            "ATOME": {
                "label": "Atome",
                "fee": {"type": "percent", "value": 5.0},
            },
            "INDODANA": {
                "label": "Indodana",
                "fee": {"type": "percent", "value": 2.3},
            },
            "KREDIVO": {
                "label": "Kredivo",
                "fee": {"type": "percent", "value": 2.3},
            },
            "UANGME": {
                "label": "UangMe",
                "fee": {"type": "percent", "value": 1.8},
            },
        },
    },
]
