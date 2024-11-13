from tortoise.contrib.pydantic import pydantic_model_creator

from database.models import PhoneBill


PhoneBillInSchema = pydantic_model_creator(
    PhoneBill, name='PhoneBillIn', exclude_readonly=True
)
PhoneBillOutSchema = pydantic_model_creator(PhoneBill, name='PhoneBillOut')
PhoneBillDatabaseSchema = pydantic_model_creator(PhoneBill, name='PhoneBill')
