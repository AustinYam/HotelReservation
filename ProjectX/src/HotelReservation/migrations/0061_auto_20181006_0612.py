# Generated by Django 2.0.4 on 2018-10-06 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0060_auto_20181005_0502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='date_in',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='date_out',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='max_number_of_guests',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='room',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='room_type',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='total_days',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
        migrations.AddField(
            model_name='reservation',
            name='charge_id',
            field=models.CharField(default='', max_length=234),
        ),
    ]
