# Generated by Django 5.0.7 on 2025-02-01 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penalties', '0002_remove_penalty_case_penalty_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='penalty',
            name='comment',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
