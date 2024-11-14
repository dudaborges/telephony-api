from tortoise.contrib.pydantic import pydantic_model_creator

from database.models import CallRecord

CallRecordInSchema = pydantic_model_creator(
    CallRecord, name='CallRecordIn', exclude_readonly=True
)
CallRecordOutSchema = pydantic_model_creator(CallRecord, name='CallRecordOut')
CallRecordDatabaseSchema = pydantic_model_creator(
    CallRecord, name='CallRecord'
)
