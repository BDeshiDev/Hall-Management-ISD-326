# Generated by Django 4.0.2 on 2022-02-19 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RoomAllotment', '0008_alter_roomallotmentrequest_requestedroomno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomallotmentrequest',
            name='stdID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomAllotment.student'),
        ),
    ]
