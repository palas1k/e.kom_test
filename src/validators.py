import re
from datetime import datetime

from starlette.requests import Request
from uvicorn.main import logger

date_formats: tuple[str, str] = ('%d.%m.%Y', '%Y-%m-%d')
regex_phone_number: str = r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
regex_email: str = r'^\w+\.*\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'


class Type:
    DATE_TYPE = 'date'
    PHONE_NUMBER_TYPE = 'phone'
    EMAIL_TYPE = 'emai'
    TEXT_TYPE = 'text'


async def validate_data(data: dict) -> dict[str, str]:
    return {name: validate(value) for name, value in data.items()}


def validate(value: str) -> str:
    if is_date(value):
        return Type.DATE_TYPE
    if is_phone_number(value):
        return Type.PHONE_NUMBER_TYPE
    if is_email(value):
        return Type.EMAIL_TYPE
    return Type.TEXT_TYPE


def is_date(value: str) -> bool:
    for format in date_formats:
        try:
            return bool(datetime.strptime(value, format))
        except ValueError:
            pass
    return False


def is_phone_number(value: str) -> bool:
    return _fullmatch(regex_phone_number, value)


def is_email(value: str) -> bool:
    return _fullmatch(regex_email, value)


def _fullmatch(pattern: str, value: str) -> bool:
    return bool(re.fullmatch(re.compile(pattern), value))
