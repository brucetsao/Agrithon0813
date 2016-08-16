# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 02:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlanName', models.CharField(max_length=255)),
                ('LocationName', models.CharField(max_length=100)),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('TimeStart', models.DateTimeField(blank=True)),
                ('TimeEnd', models.DateTimeField(blank=True)),
                ('Description', models.CharField(blank=True, max_length=255)),
                ('PhotoPath', models.CharField(blank=True, max_length=512)),
                ('Type', models.CharField(blank=True, choices=[('景點', '景點'), ('購物', '購物'), ('住宿', '住宿'), ('用餐', '用餐')], max_length=50)),
                ('dayCount', models.IntegerField(blank=True, default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TripMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TripName', models.CharField(max_length=255)),
                ('MainLocation', models.CharField(max_length=100)),
                ('Description', models.CharField(blank=True, max_length=512)),
                ('DateStart', models.DateField(blank=True)),
                ('DateEnd', models.DateField(blank=True)),
                ('TopPhoto', models.CharField(blank=True, max_length=512)),
                ('TotalDay', models.IntegerField(blank=True, default=1)),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tour.TripMain'),
        ),
    ]