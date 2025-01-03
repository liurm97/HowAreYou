# Generated by Django 5.1.4 on 2024-12-26 16:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_resource_url_alter_student_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="url",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="id",
            field=models.CharField(
                db_index=True,
                default=uuid.UUID("6560bb7a-daaa-4df6-aca1-2b96212c4a39"),
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
