# Generated by Django 2.2.8 on 2020-08-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200801_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(default='f3febf12170970ea6d6a', max_length=255, verbose_name='Key for email tracking'),
        ),
    ]
