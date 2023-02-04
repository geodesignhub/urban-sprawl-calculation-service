from django.db import models
from datetime import datetime
import uuid
# Create your models here.

class WUPCalculation(models.Model):
    processing_id = models.UUIDField(default=uuid.uuid4, unique=True)
    dis = models.DecimalField(max_digits=12,decimal_places=10)
    lup = models.DecimalField(max_digits=12,decimal_places=10)
    wup = models.DecimalField(max_digits=12,decimal_places=10)
    resident_count_in_boundary = models.IntegerField(default=0, help_text="Enter the expected number of residents in the vector boundary provided.")
    employment_count_in_boundary = models.IntegerField(default=0, help_text="Enter the expected number of employees in the vector boundary provided.")
    raster_with_build_up_area = models.URLField(help_text="The public URL at which the the raster with build up / non-build up values shall be downloaded from.")
    raster_no_data_value = models.IntegerField(default=0, help_text="Enter the `nodata` value in the Raster, expected 0.")
    raster_build_up_value = models.IntegerField(default=1, help_text="Enter the build up value in the raster, normally 1, see the documentation regarding representing built up / non-built up areas in a raster.")
    vector_boundary = models.JSONField(help_text="Enter the boundary in GeoJSON format")
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