# Generated by Django 4.1.5 on 2023-03-07 09:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WUPCalculation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dis', models.DecimalField(decimal_places=10, help_text='Computed DIS value for the dataset', max_digits=12)),
                ('lup', models.DecimalField(decimal_places=10, help_text='Computed LUP value for the dataset', max_digits=12)),
                ('wup', models.DecimalField(decimal_places=10, help_text='Computed WUP value for the dataset', max_digits=12)),
                ('resident_count_in_boundary', models.IntegerField(default=0, help_text='Enter the expected number of residents in the vector boundary provided.')),
                ('employment_count_in_boundary', models.IntegerField(default=0, help_text='Enter the expected number of employees in the vector boundary provided.')),
                ('raster_with_build_up_area', models.URLField(help_text='The public URL at which the the raster with build up / non-build up values shall be downloaded from.')),
                ('raster_no_data_value', models.IntegerField(default=0, help_text='Enter the `nodata` value in the Raster, expected 0.')),
                ('raster_build_up_value', models.IntegerField(default=1, help_text='Enter the build up value in the raster, normally 1, see the documentation regarding representing built up / non-built up areas in a raster.')),
                ('vector_boundary', models.JSONField(help_text='Enter the boundary in GeoJSON format')),
                ('share_of_settlement_area', models.DecimalField(decimal_places=5, help_text='Share of Settlement area  for the raster', max_digits=12)),
                ('status', models.CharField(choices=[('Activating', 'Activating'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Rejected', 'Rejected'), ('Error', 'Error')], default='Activating', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
