# Generated by Django 3.2.4 on 2021-08-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configportal',
            name='value',
            field=models.CharField(max_length=70),
        ),
    ]
