# Generated by Django 3.0.3 on 2020-03-07 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasyworld', '0003_auto_20200307_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='is_commissioner',
            field=models.BooleanField(default=False),
        ),
    ]
