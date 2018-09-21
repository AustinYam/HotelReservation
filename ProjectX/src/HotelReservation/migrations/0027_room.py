# Generated by Django 2.0.4 on 2018-09-08 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HotelReservation', '0026_auto_20180908_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RoomType', models.CharField(max_length=255)),
                ('Capacity', models.IntegerField(default=0)),
                ('BedOption', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('TotalRooms', models.CharField(max_length=255)),
                ('check_in', models.DateField(auto_now_add=True)),
                ('check_out', models.DateField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelReservation.HotelList')),
            ],
            options={
                'verbose_name_plural': 'Room',
            },
        ),
    ]