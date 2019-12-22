from .helpers import post


def queue_draft(
    author_email, subject, body,
    shared_channel_address, to_array=None
):
    route = f'/channels/alt:address:{shared_channel_address}/drafts'

    data = {
        'author_id': f'alt:email:{author_email}',
        'subject': subject,
        'body': body
    }

    if to_array is not None:
        data['to'] = to_array

    post(json=data, route=route, max_attempts=2)

    return
