# Generated by Django 5.1.4 on 2024-12-25 04:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[("article", "Article"), ("video", "Video")],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            ("type", "article"), ("type", "video"), _connector="OR"
                        ),
                        name="Type constraint",
                        violation_error_message="Type must be one of 'article' or 'video'.",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("url__length__gt", 0)),
                        name="URL constraint",
                        violation_error_message="URL cannot be empty string.",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_index=True,
                        default=uuid.UUID("8585dbe7-a361-475a-9178-7b665eef7f11"),
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                        max_length=1,
                    ),
                ),
                ("age", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("age__gte", 12), ("age__lte", 24)),
                        name="Age constraint",
                        violation_error_message="Age must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            ("gender", "M"),
                            ("gender", "F"),
                            ("gender", "O"),
                            _connector="OR",
                        ),
                        name="Gender constraint",
                        violation_error_message="Gender must be one of 'M', 'F', 'O'.",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="StudentResponse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("q1_resp", models.IntegerField()),
                ("q2_resp", models.IntegerField()),
                ("q3_resp", models.IntegerField()),
                ("q4_resp", models.IntegerField()),
                ("q5_resp", models.IntegerField()),
                ("q6_resp", models.IntegerField()),
                ("q7_resp", models.IntegerField()),
                ("q8_resp", models.IntegerField()),
                ("q9_resp", models.IntegerField()),
                ("score", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student",
                        to="api.student",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("q1_resp__gte", 0), ("q1_resp__lte", 3)),
                        name="q1_resp constraint",
                        violation_error_message="q1_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q2_resp__gte", 0), ("q2_resp__lte", 3)),
                        name="q2_resp constraint",
                        violation_error_message="q2_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q3_resp__gte", 0), ("q3_resp__lte", 3)),
                        name="q3_resp constraint",
                        violation_error_message="q3_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q4_resp__gte", 0), ("q4_resp__lte", 3)),
                        name="q4_resp constraint",
                        violation_error_message="q4_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q5_resp__gte", 0), ("q5_resp__lte", 3)),
                        name="q5_resp constraint",
                        violation_error_message="q5_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q6_resp__gte", 0), ("q6_resp__lte", 3)),
                        name="q6_resp constraint",
                        violation_error_message="q6_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q7_resp__gte", 0), ("q7_resp__lte", 3)),
                        name="q7_resp constraint",
                        violation_error_message="q7_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q8_resp__gte", 0), ("q8_resp__lte", 3)),
                        name="q8_resp constraint",
                        violation_error_message="q8_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("q9_resp__gte", 0), ("q9_resp__lte", 3)),
                        name="q9_resp constraint",
                        violation_error_message="q9_resp must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("score__gte", 0), ("score__lte", 27)),
                        name="score constraint",
                        violation_error_message="score must be between 12 (inclusive) and 24 (inclusive).",
                    ),
                ],
            },
        ),
    ]
