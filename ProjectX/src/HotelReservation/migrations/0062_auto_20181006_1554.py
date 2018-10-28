# Generated by Django 2.0.4 on 2018-10-06 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HotelReservation', '0061_auto_20181006_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='charge_id',
        ),
        migrations.AddField(
            model_name='reservation',
            name='date_in',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='date_out',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='hotel',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='HotelReservation.HotelList'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='reservation',
            name='max_number_of_guests',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='HotelReservation.Room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room_type',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
