import logging

import requests

logger = logging.getLogger('accounts')


def send_msg(phone_number, message):
    data = {
        "data": [
            {
                "text": message,
                "phone_numbers": [phone_number]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Token {random token of gate way}"
    }
    r = object

    try:
        r = requests.post(
            headers=headers,
            url='SMS_GATE_WAY_URL',
            json=data,
            timeout=(3, 6)
        )
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.error(
            f"[HTTP exception occurred while sending SMS]"
            f"-[func-name: {send_msg.__name__}]"
            f"-[response: {r.content}]"
            f"-[phone-number: {phone_number}]"
            f"-[error: {e}]"
            f"-[message: {message}]"
        )
        return False
    except Exception as e:
        logger.error(
            f"[Bare exception occurred while sending SMS]"
            f"-[func-name: {send_msg.__name__}]"
            f"-[phone-number: {phone_number}]"
            f"-[error: {e}]"
            f"-[message: {message}]"
        )
        return False
    logger.info(
        f"[SMS sent successfully]"
        f"-[func-name: {send_msg.__name__}]"
        f"-[response: {r.content}]"
        f"-[phone-number: {phone_number}]]"
        f"-[message: {message}]"
    )
    return True
