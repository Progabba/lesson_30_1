# Generated by Django 5.1.3 on 2024-12-17 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
