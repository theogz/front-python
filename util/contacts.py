from .helpers import get


def fetch_contact(handle):
    route = f'/contacts/alt:email:{handle}'

    return get(route, attempt=1, max_attempts=1)
