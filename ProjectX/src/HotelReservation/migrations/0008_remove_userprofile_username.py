# Generated by Django 2.0.4 on 2018-08-25 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0007_auto_20180825_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
