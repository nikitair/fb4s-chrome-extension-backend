
def na_formatter(raw_payload: dict):
    for key, value in raw_payload.items():
        raw_payload[key] = value if value != "N/A" else ""
    return raw_payload


def format_postalcode(postalcode: str):
    """
    formats postalcode into desired format -- A1A1A1 -> A1A 1A1
    """
    res = ''
    if isinstance(postalcode, str):
        if len(postalcode) > 0:
            if len(postalcode) == 6:
                res = f"{postalcode[0:3]} {postalcode[3:6]}"
            else:
                res = postalcode
    return res.upper()
