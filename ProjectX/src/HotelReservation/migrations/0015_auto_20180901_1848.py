# Generated by Django 2.0.4 on 2018-09-01 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0014_auto_20180901_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotellist',
            name='room_type',
            field=models.CharField(choices=[('Single', 'SINGLE'), ('Double', 'DOUBLE')], default='', max_length=100),
        ),
    ]