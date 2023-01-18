from django.db import models
from datetime import datetime
import uuid
# Create your models here.

class WUPCalculation(models.Model):
    uuid = models.UUIDField(max_length=36, min_length=36, format='uuid', default=uuid.uuid4, unique=True)
    resident_count_in_boundary = models.IntegerField()
    employment_count_in_boundary = models.IntegerField()
    raster_with_build_up_area = models.URLField()
    raster_no_data_value = models.IntegerField()
    raster_build_up_value = models.IntegerField()
    vector_boundary = models.PolygonField()
    status = models.CharField(
        max_length=255,
        choices=[
            ('Activating', 'Activating'),
            ('Processing', 'Processing'),
            ('Completed', 'Completed'),
            ('Rejected', 'Rejected'),
            ('Error', 'Error')
        ],
        default='Activating'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)