from database.models import PhoneBill, CallRecord
from datetime import datetime, timedelta

async def generate_bill(phone_number, period):
    start_period = datetime.strptime(f"01/{period}", "%d/%m/%Y")
    end_period = start_period + timedelta(days=30) 

    records = await CallRecord.filter(
        source=phone_number,
        timestamp__gte=start_period,
        timestamp__lt=end_period
    )

    total_cost = 0
    for record in records:
        duration = (record.end_time - record.start_time).total_seconds()
        if record.start_time.hour >= 6 and record.start_time.hour < 22:
            cost = 0.36 + (duration // 60) * 0.09
        else:
            cost = 0.36
        total_cost += cost

    bill = await PhoneBill.create(
        phone_number=phone_number,
        period=start_period,
        total_cost=total_cost,
    )
    return bill
