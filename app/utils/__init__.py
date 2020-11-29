import uuid


def generate_random_trace_id() -> str:
    return uuid.uuid4().hex
