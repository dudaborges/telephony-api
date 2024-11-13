from fastapi import APIRouter
from schemas.call_record import CallRecordOutSchema, CallRecordInSchema
from schemas.status import Status
import crud.call_record as crud
from typing import List
from tortoise.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get('/call_records', response_model=List[CallRecordOutSchema])
async def test():
    return await crud.get_call_records()

@router.get('/call_record/{call_record_id}', response_model=CallRecordOutSchema)
async def get_message(call_record_id: str) -> CallRecordOutSchema:
    try:
        logging.info(f'Get call record {call_record_id}')
        return await crud.get_call_record(call_record_id)
    except DoesNotExist:
        logging.error(f'Call record {call_record_id} does not exist')
        raise HTTPException(status_code=404, detail="Call record does not exist")

@router.post('/create', response_model=CallRecordOutSchema)
async def create_message(call_record: CallRecordInSchema):
    return await crud.create_call_record(call_record)

@router.delete('/call_record/{call_record_id}', response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_message(call_record_id: str) -> Status:
    return await crud.delete_message(call_record_id)
