# Generated by Django 3.0.3 on 2020-04-05 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fantasyworld', '0014_stock_stock_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaguetype',
            old_name='positions',
            new_name='stock_types',
        ),
    ]
