# Generated by Django 4.0.1 on 2022-03-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_rename_notifactionstatus_notification_notificationstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='entity_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]