from tokenize import blank_re
from django.db import models
import uuid
from django.db.models import UniqueConstraint
from call_applications.models import CallForApplication 
from user.models import User

class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    room = models.CharField(max_length=100, blank=False, null=False)
    capacity = models.IntegerField(default=0, blank=False, null=False)
    call_for_application = models.ForeignKey(CallForApplication, on_delete=models.SET_NULL, null=True, blank=True)


class Transaction(models.Model):
    TYPE_CHOICE= (
        ('Manual', "Manual"),
        ("Gateway", "Gateway"),
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    payment_type = models.CharField(max_length=10, choices=TYPE_CHOICE,  null=False, blank=False)
    transaction_method = models.CharField(max_length=100, blank=False, null=False)
    amount = models.CharField(max_length=100, blank=False, null=False)
    transaction_from = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, blank=False, null=False)
    transaction_time = models.DateField(max_length=100, blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)        



class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    call_for_application = models.ForeignKey(CallForApplication, on_delete=models.CASCADE, null=False, blank=False)
    roll_no = models.CharField(max_length=20, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)   
    data = models.JSONField(editable=False)
    is_approved = models.BooleanField(default=False)
    is_payment_done = models.BooleanField(default=False)
    gw_trx_id = models.CharField(max_length=100, null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, blank=True)
    is_admit_ready = models.BooleanField(default=False)
    is_seatplan_ready = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together= [['call_for_application', 'user']]
        ordering = ('roll_no',)

class PageRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "P", "Pending"
        GENERATING = "G", "Generating"
        READY = "R", "Ready"
        ERROR = "E", "Error"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
    error_msg = models.CharField(max_length=128, blank=True, null=True)
    pdf_file = models.FileField(upload_to=f"pdfs", null=True, blank=True)
    template_src = models.CharField(max_length=200, null=False, blank=False)
    base_url = models.CharField(max_length=200, null=False, blank=False)
    context = models.CharField(max_length=200, null=False, blank=False)
    season = models.CharField(max_length=200, null=False, blank=False)
