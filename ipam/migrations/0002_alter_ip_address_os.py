# Generated by Django 3.2.4 on 2021-07-19 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip_address',
            name='os',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.os'),
        ),
    ]
