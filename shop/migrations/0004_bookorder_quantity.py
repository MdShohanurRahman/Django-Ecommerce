# Generated by Django 2.0.6 on 2019-01-27 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_bookorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookorder',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]