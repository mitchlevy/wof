# Generated by Django 3.0.3 on 2020-04-15 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantasyworld', '0015_auto_20200405_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguetype',
            name='meta_leaguetype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fantasyworld.LeagueType'),
        ),
    ]