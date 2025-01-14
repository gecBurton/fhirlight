def prepare_payload(payload: dict):
    payload["active"] = payload.get("active", True)
    return payload
