
def na_formatter(raw_payload: dict):
    for key, value in raw_payload.items():
        raw_payload[key] = value if value != "N/A" else ""
    return raw_payload
