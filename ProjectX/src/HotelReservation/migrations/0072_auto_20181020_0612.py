# Generated by Django 2.0.4 on 2018-10-20 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0071_photoforteam_roles2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestchoice',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='bestchoice',
            name='user',
        ),
        migrations.DeleteModel(
            name='BestChoice',
        ),
    ]
