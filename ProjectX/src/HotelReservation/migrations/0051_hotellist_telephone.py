# Generated by Django 2.0.4 on 2018-09-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0050_remove_hotellist_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotellist',
            name='telephone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
