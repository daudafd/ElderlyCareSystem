# Generated by Django 3.2.3 on 2024-07-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0003_auto_20240710_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
    ]
