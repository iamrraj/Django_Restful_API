# Generated by Django 2.2 on 2020-02-20 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]