# Generated by Django 4.0.2 on 2022-02-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomAllotment', '0006_alter_provost_mobile_no_alter_student_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='gotoURL',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]