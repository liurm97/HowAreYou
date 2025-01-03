# Generated by Django 5.1.4 on 2024-12-29 01:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_remove_student_gender_constraint_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.UUID("bfd28c98-29cc-4b7f-915d-a9e64714b637"),
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
