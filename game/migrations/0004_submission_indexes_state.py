# Generated by Django 3.1.4 on 2021-08-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_submission_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='indexes_state',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
