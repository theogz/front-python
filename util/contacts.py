from .helpers import get


def fetch_contact(contact_id):
    route = f'/contacts/{contact_id}'

    return get(route, attempt=1, max_attempts=1)
