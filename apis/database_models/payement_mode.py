from django.db import models


class PaymentMode(models.Model):
    payment_id = models.AutoField(primary_key=True, db_column='payment_id')
    payment_mode = models.CharField(
        max_length=250, null=True, db_column='payment_mode')

    class Meta:
        db_table = 'payment_mode'
