# Generated by Django 2.0.4 on 2018-09-11 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0035_auto_20180911_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='view',
        ),
    ]
