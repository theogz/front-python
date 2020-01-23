import os
import requests
import time

# Front API helpers
FRONT_API_TOKEN = os.getenv('FRONT_API_JWT')
FRONT_HEADERS = {'Authorization': f'Bearer {FRONT_API_TOKEN}'}
FRONT_BASE_URL = 'https://api2.frontapp.com'


def log(*args, **kwargs):
    return print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} -', *args, **kwargs)


def front_decorator(front_function):
    def wrapper(*args, **kwargs):
        try:
            output = front_function(*args, **kwargs)
            log(f'[OK] - "{front_function.__name__}"')
            return output
        except Exception as e:
            log(f'[ERROR] - "{front_function.__name__}":')
            print(e)
            return None
    return wrapper


def post(route, attempt=1, max_attempts=1, **kwargs):
    '''
    Returns tuple with (status code, error message)
    '''
    assert attempt <= max_attempts, 'Problem with "attempts" parameters'
    URL = f'{FRONT_BASE_URL}{route}'

    log(f'POST {URL}')
    r = requests.post(url=URL, headers=FRONT_HEADERS, **kwargs)

    # Success.
    if r.status_code < 400:
        log(f'[OK] - status code: {r.status_code}')
        return r.status_code, None

    # Max attempts or 4xx error.
    if r.status_code < 500 or attempt == max_attempts:
        log(f'[ERROR] - status code: {r.status_code} - {r.text}')
        return r.status_code, r.text

    # Try one more time.
    next_attempt = attempt + 1
    log(
        f'[WARNING] - status code: {r.status_code} - {r.text}, '
        f'retrying ({next_attempt} / {max_attempts})'
    )
    return post(route=route, attempt=next_attempt, max_attempts=max_attempts, **kwargs)


def get(route, attempt=1, max_attempts=1, **kwargs):
    '''
    Returns tuple with (body, status code, error message)
    '''
    assert attempt <= max_attempts, 'Problem with "attempts" parameters'
    URL = f'{FRONT_BASE_URL}{route}'

    log(f'GET {URL}')
    r = requests.get(url=URL, headers=FRONT_HEADERS, **kwargs)

    # Success.
    if r.status_code < 400:
        log(f'[OK] - status code: {r.status_code}')
        return r.json(), r.status_code, None

    # Max attempts or 4xx error.
    if r.status_code < 500 or attempt == max_attempts:
        log(f'[ERROR] - status code: {r.status_code} - {r.text}')
        return None, r.status_code, r.text

    # Try one more time.
    next_attempt = attempt + 1
    log(
        f'[WARNING] - status code: {r.status_code} - {r.text}, '
        f'retrying ({next_attempt} / {max_attempts})'
    )
    return get(route=route, attempt=next_attempt, max_attempts=max_attempts, **kwargs)
