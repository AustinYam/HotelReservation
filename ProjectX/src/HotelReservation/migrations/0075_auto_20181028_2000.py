# Generated by Django 2.0.4 on 2018-10-28 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0074_auto_20181027_0518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_detail',
        ),
        migrations.AddField(
            model_name='room',
            name='room_detail1',
            field=models.TextField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='room',
            name='room_detail2',
            field=models.TextField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='room',
            name='room_detail3',
            field=models.TextField(blank=True, default='', max_length=255),
        ),
    ]
