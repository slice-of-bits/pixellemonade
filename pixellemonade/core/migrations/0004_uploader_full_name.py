# Generated by Django 4.1.7 on 2023-03-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_photoview_photodownload'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploader',
            name='full_name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]