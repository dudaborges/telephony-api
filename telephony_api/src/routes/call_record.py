import logging
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import crud.call_record as crud
from database.models import PhoneBill
from schemas.call_record import CallRecordInSchema, CallRecordOutSchema
from schemas.phone_bill import PhoneBillDatabaseSchema
from schemas.status import Status

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get('/call_records', response_model=List[CallRecordOutSchema])
async def test():
    return await crud.get_call_records()


@router.get(
    '/call_record/{call_record_id}', response_model=CallRecordOutSchema
)
async def get_message(call_record_id: str) -> CallRecordOutSchema:
    try:
        logging.info(f'Get call record {call_record_id}')
        return await crud.get_call_record(call_record_id)
    except DoesNotExist:
        logging.error(f'Call record {call_record_id} does not exist')
        raise HTTPException(
            status_code=404, detail='Call record does not exist'
        )


@router.post('/create', response_model=CallRecordOutSchema)
async def create_message(call_record: CallRecordInSchema):
    return await crud.create_call_record(call_record)


@router.delete(
    '/call_record/{call_record_id}',
    response_model=Status,
    responses={404: {'model': HTTPNotFoundError}},
)
async def delete_message(call_record_id: str) -> Status:
    return await crud.delete_message(call_record_id)


@router.get(
    '/phone-bill/{phone_number}', response_model=PhoneBillDatabaseSchema
)
async def get_phone_bill(phone_number: str, period: str = None):
    if not period:
        period = (datetime.now() - timedelta(days=30)).strftime('%m/%Y')

    bill = await crud.generate_bill(phone_number, period)

    if not bill:
        raise HTTPException(status_code=404, detail='Bill not found')

    bill_with_records = await PhoneBill.filter(id=bill.id).prefetch_related(
        'records'
    )
    return await PhoneBillDatabaseSchema.from_tortoise_orm(
        bill_with_records[0]
    )
