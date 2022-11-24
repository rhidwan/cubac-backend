from tokenize import blank_re
from django.db import models
from django_resized import ResizedImageField
import uuid
from user.models import User


# Create your models here.
class EducationalBackground(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educational_background", related_query_name="educational_background")
    degree = models.CharField(max_length=100, blank=False, null=False)
    institute = models.CharField(max_length=100, blank=False, null=False)
    passing_year = models.CharField(max_length=50, blank=True, null=True)
    area_major = models.CharField(max_length=100, blank=False, null=False)
    division_class_cgpa = models.CharField(max_length=100, blank=True, null=True)

class WorkExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_experience")
    post = models.TextField(null=False, blank=False)
    organization = models.CharField(max_length=100, null=False, blank=False)
    major_responsibilities = models.TextField(null=True, blank=True )
    from_date = models.CharField(max_length=100, null=False, blank=False)
    to_date = models.CharField(max_length=100, null=True, blank=True)
    is_current = models.BooleanField()

class AchievementMembership(models.Model):
    TYPE_CHOICE = (
        ('Membership', 'Membership'),
        ('Achievement', 'Achievement'),
        ('Award', 'Award')
        )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievement_membership")
    achievement_type = models.CharField(max_length=20, choices=TYPE_CHOICE, null=False, blank=False)
    organization = models.CharField(max_length=250, null=False, blank=False)
    year = models.CharField(max_length=50, blank=False, null=False)

class TestScore(models.Model):
    EXAM_CHOICE= (
        ('GMAT', "GMAT"),
        ("GRE", "GRE"),
        ("TOEFL", "TOEFL"),
        ("IELTS", "IELTS")
        )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_score")
    test = models.CharField(max_length=10, choices=EXAM_CHOICE,  null=False, blank=False)
    score = models.CharField(max_length=20, null=False, blank=False)
    test_date = models.DateField(null=False, blank=False)
    
class BasicInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basic_info")
    father_name = models.CharField(max_length=250, null=False, blank=False)
    mother_name = models.CharField(max_length=250, null=False, blank=False)
    nationality = models.CharField(max_length=100, null=False, blank=False)
    nid_passport_no = models.CharField(max_length=250, null=False, blank=False)
    is_employed = models.BooleanField(blank=False, null=False)
    permanent_address = models.TextField()
    present_address = models.TextField()
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    work_phone = models.CharField(max_length=50, null=True, blank=True)
    photo = ResizedImageField(size=[300,300], upload_to="pictures/")

