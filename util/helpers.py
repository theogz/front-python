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


def post(*args, attempt=1, max_attempts=1, **kwargs):
    '''
    Returns None (success) or Exception (failure)
    '''

    # attempt = kwargs.get('attempt', 1)
    # max_attempts = kwargs.get('max_attempts', 1)
    assert attempt <= max_attempts, 'Problem with "attempts" parameters'

    r = requests.post(*args, **kwargs)
    print(f'POST {r.url}')

    if r.status_code < 400:
        print(f'[OK] - status code: {r.status_code}')
        return

    if r.status_code < 500 or attempt == max_attempts:
        print(f'[ERROR] - status code: {r.status_code} ({r.text})')
        raise requests.exceptions.HTTPError(r.status_code)

    next_attempt = attempt + 1
    print(
        f'[WARNING] - status code: {r.status_code} ({r.text}), '
        f'retrying ({next_attempt} / {max_attempts})'
    )
    return post(*args, attempt=next_attempt, max_attempts=max_attempts, **kwargs)


def queue_draft(
    author_email, subject, body,
    shared_channel_address, to_array=None
):
    url = f'{FRONT_BASE_URL}/channels/alt:address:{shared_channel_address}/drafts'

    data = {
        'author_id': f'alt:email:{author_email}',
        'subject': subject,
        'body': body
    }

    if to_array is not None:
        data['to'] = to_array

    post(url, json=data, headers=FRONT_HEADERS)

    return
