from django.db import models

# Create your models here.

class WUPCalculation(models.Model):
    uuid = models.UUIDField(max_length=36, min_length=36, format='uuid', default=uuid.uuid4, unique=True)
    WUPCalculationRequestStatus = models.CharField(
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
    