import re


def verify_worker_id(worker_id):
    if len(worker_id) >= 10 and len(worker_id) <= 16:
        if re.match("[A-Z0-9]*", worker_id):
            return True
    return False
