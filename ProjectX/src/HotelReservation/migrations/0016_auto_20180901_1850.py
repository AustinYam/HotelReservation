# Generated by Django 2.0.4 on 2018-09-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0015_auto_20180901_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotellist',
            name='room_type',
            field=models.CharField(choices=[('ONEBED', 'Single'), ('TWOBEDS', 'Double')], default='', max_length=100),
        ),
    ]
