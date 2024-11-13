from tortoise import fields, models


class CallRecord(models.Model):
    id = fields.UUIDField(pk=True)
    type = fields.CharField(max_length=10)
    timestamp = models.DateTimeField(null=False)
    call_id = fields.IntField()
    source = models.CharField(max_length=15, null=True)
    destination = models.CharField(max_length=15, null=True)


class PhoneBill(models.Model):
    id = fields.UUIDField(pk=True)
    phone_number = fields.CharField(max_length=15) 
    period = fields.DateField()
    total_cost = fields.DecimalField(max_digits=10, decimal_places=2) 
    records = fields.ManyToManyField('models.CallRecord', related_name='phone_bill')
