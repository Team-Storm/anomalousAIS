from django.db import models

# Create your models here.
class Data(models.Model):
   name = models.CharField(max_length = 50)
   file = models.FileField(upload_to = 'data')

   class Meta:
      db_table = "data"