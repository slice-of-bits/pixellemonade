# Generated by Django 4.1.7 on 2023-03-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image_hash',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]