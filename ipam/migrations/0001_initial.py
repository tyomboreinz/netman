# Generated by Django 3.2.4 on 2021-08-25 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigPortal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(max_length=25)),
                ('value', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Dhcp_Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dhcp_static',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('mac', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ip_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=15)),
                ('hostname', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netmask', models.CharField(max_length=15)),
                ('ip_network', models.CharField(max_length=15)),
                ('ip_broadcast', models.CharField(max_length=15)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SubDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=5)),
                ('description', models.TextField()),
                ('ip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.ip_address')),
                ('root_domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipam.domain')),
            ],
        ),
        migrations.AddField(
            model_name='ip_address',
            name='os',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.os'),
        ),
        migrations.AddField(
            model_name='ip_address',
            name='subnet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipam.subnet'),
        ),
        migrations.AddField(
            model_name='domain',
            name='ip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.ip_address'),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('protocol', models.CharField(max_length=5)),
                ('port', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='app/')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ipam.ip_address')),
            ],
        ),
    ]
