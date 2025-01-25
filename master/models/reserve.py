from django.db import models

class Reserve(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    ip_address = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    reserve_date = models.DateTimeField()
    person = models.CharField(max_length=15)
    memo= models.CharField(max_length=50)
    seat_type = models.IntegerField()
    smoke = models.BooleanField()
    saas_id = models.CharField(max_length=32)
    status  = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reserve'