# Generated by Django 5.1.6 on 2025-04-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("UserProfile", "0003_baskets"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.CharField(default=None, max_length=255),
        ),
    ]
