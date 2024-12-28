# Generated by Django 5.1.4 on 2024-12-26 15:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_student_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="url",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="student",
            name="id",
            field=models.CharField(
                db_index=True,
                default=uuid.UUID("3d237f4c-0dd7-47e4-9e25-766a9addf22e"),
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]