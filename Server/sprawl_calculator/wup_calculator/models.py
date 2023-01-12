from django.db import models
import uuid

# Create your models here.

class Model(models.Model):
	id = models.UUIDField() #Id
	field1 = models.CharField() #Character
	field2 = models.DateTimeField() #Time
	status = models.IntegerField() #Status

	def __str__(self):
        return self.id
