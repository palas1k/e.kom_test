from urllib.request import Request

from uvicorn.main import logger

from src.validators import validate_data


async def find_match(request: Request, data: dict[str, str]):
    templates: list[dict] = list(request.app.database['templates'].find())
    matched_template = None
    for template in templates:
        template_fields = {k: v for k, v in template.items() if k not in ('_id', 'name')}
        if all(field in data and data[field] == template_fields[field] for field in template_fields):
            matched_template = template['name']
            break

    if matched_template:
        return matched_template

    return await validate_data(data)
