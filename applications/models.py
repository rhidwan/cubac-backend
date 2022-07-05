from django.db import models
import uuid
from django.db.models import UniqueConstraint
from call_applications.models import CallForApplication 
from user.models import User


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    call_for_application = models.ForeignKey(CallForApplication, on_delete=models.CASCADE, null=False, blank=False)
    roll_no = models.CharField(max_length=20, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)   
    data = models.JSONField(editable=False)
    is_approved = models.BooleanField(default=False)
    is_payment_done = models.BooleanField(default=False)
    gw_trx_id = models.CharField(max_length=100, null=True, blank=True)
    seat = models.CharField(max_length=100, null=True, blank=True)

    # class Meta:
    #    unique_together= [['call_for_application', 'user']]