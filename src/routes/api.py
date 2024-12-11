from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.utils import find_match

router = APIRouter()


@router.post("/get_form")
async def get_template(request: Request,
                       data: dict[str, str]):
    if data == {}:
        return JSONResponse(
            content={'ERROR': 'Form is empty'},
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )

    result = await find_match(request, data)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@router.post("/set_data")
async def set_data(request: Request, data: dict[str, str]):
    request.app.database['templates'].insert_one(data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'success': True})
