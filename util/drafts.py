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

    return post(json=data, route=route, max_attempts=2)


def create_draft_reply(
    conversation_id, author_email, shared_channel_address,
    body
):
    route = f'/conversations/{conversation_id}/drafts'

    data = {
        'channel_id': f'alt:address:{shared_channel_address}',
        'author_id': f'alt:email:{author_email}',
        'body': body
    }

    return post(json=data, route=route, max_attempts=1)
