# Generated by Django 3.1.7 on 2021-03-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210303_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
