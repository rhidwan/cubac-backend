from django.db import models
import uuid


# Create your models here.
class CallForApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False)
    description = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    is_open = models.BooleanField(default=False)
    shortcode = models.CharField(max_length=10, blank=False, null=False)

    
