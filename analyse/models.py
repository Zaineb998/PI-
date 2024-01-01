from django.db import models
import uuid
from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
# Create your models here.

def random_date_2022_2023():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_days = randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

class Data(models.Model):
    titre=models.CharField(max_length=255)
    paragraph= models.TextField()
    predicted_pabel= models.CharField('Predicted Pabel',max_length=255)
    scores=models.FloatField(default=0)
    sentiment = models.CharField(max_length=255)
    uuid=models.CharField(max_length=255)
    release_date = models.DateField(default=random_date_2022_2023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)