# Generated by Django 3.1.5 on 2021-01-31 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0004_auto_20210131_0132"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="%Y/%m/%d"),
        ),
    ]
