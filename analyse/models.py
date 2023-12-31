from django.db import models
import uuid
# Create your models here.

class Data(models.Model):
    titre=models.CharField(max_length=255)
    paragraph= models.TextField()
    predicted_pabel= models.CharField('Predicted Pabel',max_length=255)
    scores=models.FloatField(default=0)
    sentiment = models.CharField(max_length=255)
    uuid=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)