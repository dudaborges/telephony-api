from tortoise import fields, models


class CallRecord(models.Model):
    id = fields.UUIDField(pk=True)
    type = models.CharField(max_length=10, choices=[('start', 'Start'), ('end', 'End')], null=False)
    timestamp = models.DateTimeField(null=False)
    call_id = models.CharField(max_length=255, null=False, unique=True)
    source = models.CharField(max_length=15, null=True)
    destination = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PhoneBill(models.Model):
    id = fields.UUIDField(pk=True)
    phone_number = fields.CharField(max_length=15) 
    period = fields.CharField(max_length=7) 
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2) 
    call_records = fields.ReverseRelation["CallRecord"] 