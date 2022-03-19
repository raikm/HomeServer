# Generated by Django 4.0.1 on 2022-03-18 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='status',
            new_name='notifactionStatus',
        ),
        migrations.AddField(
            model_name='notification',
            name='application',
            field=models.CharField(choices=[('PL', 'Plants'), ('DE', 'Devices')], default='PL', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('BL', 'Battery low'), ('NR', 'No Response')], max_length=100),
        ),
    ]
