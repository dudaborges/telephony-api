from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from database.models import CallRecord
from schemas.call_record import CallRecordOutSchema
from schemas.status import Status
from starlette.responses import Response
import logging

logging.basicConfig(level=logging.INFO)


async def get_call_records():
    return await CallRecordOutSchema.from_queryset(CallRecord.all())


async def get_call_record(call_record_id) -> CallRecordOutSchema:
    return await CallRecordOutSchema.from_queryset_single(
        CallRecord.get(id=call_record_id)
    )


async def create_call_record(call_record) -> CallRecordOutSchema:
    current_call_dict = call_record.dict(exclude_unset=True)
    current_call_obj = await CallRecord.create(**current_call_dict)
    return await CallRecordOutSchema.from_tortoise_orm(current_call_obj)


async def delete_message(call_record_id) -> Status:
    try:
        logging.info(f'Deleting call record {call_record_id}')
        db_call_record = await CallRecordOutSchema.from_queryset_single(
            CallRecord.get(id=call_record_id)
        )
    except DoesNotExist:
        logging.error(f'Call record id {call_record_id} does not exist')
        raise HTTPException(
            status_code=404, detail=f'Message {call_record_id} not found'
        )

    deleted_count = await CallRecord.filter(id=call_record_id).delete()
    if not deleted_count:
        logging.error(f'Call record id {call_record_id} not found')
        raise HTTPException(
            status_code=404, detail=f'Message {call_record_id} not found'
        )

    response = Response(
        content='Call log deleted successfully!', status_code=200
    )
    return response
