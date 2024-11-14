import logging
from datetime import datetime, timedelta

from fastapi import HTTPException
from starlette.responses import Response
from tortoise.exceptions import DoesNotExist

from database.models import CallRecord, PhoneBill
from schemas.call_record import CallRecordOutSchema
from schemas.status import Status

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


async def generate_bill(phone_number, period):
    start_period = datetime.strptime(f'01/{period}', '%d/%m/%Y')
    end_period = start_period + timedelta(days=30)

    records = await CallRecord.filter(
        source=phone_number,
        timestamp__gte=start_period,
        timestamp__lt=end_period,
    ).order_by('timestamp')

    total_cost = 0
    call_details = []
    call_pairs = {}

    for record in records:
        if record.call_id not in call_pairs:
            call_pairs[record.call_id] = {'start': None, 'end': None}
        if record.type == 'start':
            call_pairs[record.call_id]['start'] = record
        elif record.type == 'end':
            call_pairs[record.call_id]['end'] = record

    for call_id, pair in call_pairs.items():
        start_record = pair['start']
        end_record = pair['end']
        if not start_record or not end_record:
            continue

        duration = (
            end_record.timestamp - start_record.timestamp
        ).total_seconds()
        if (
            start_record.timestamp.hour >= 6
            and start_record.timestamp.hour < 22
        ):
            cost = 0.36 + (duration // 60) * 0.09
        else:
            cost = 0.36

        total_cost += cost
        call_details.append(
            {
                'destination': start_record.destination,
                'start_date': start_record.timestamp.date(),
                'start_time': start_record.timestamp.time(),
                'duration': f'{int(duration // 3600)}h{int((duration % 3600) // 60)}m{int(duration % 60)}s',
                'cost': round(cost, 2),
            }
        )

    phone_bill = await PhoneBill.create(
        phone_number=phone_number,
        period=start_period,
        total_cost=total_cost,
    )
    await phone_bill.records.add(
        *[
            pair['start']
            for pair in call_pairs.values()
            if pair['start'] and pair['end']
        ]
    )

    return phone_bill
