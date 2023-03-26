# Generated by Django 4.1.7 on 2023-03-24 17:13

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_photo_image_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoView',
            fields=[
                ('id', hashid_field.field.BigHashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', auto_created=True, min_length=13, prefix='', primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ip', models.GenericIPAddressField()),
                ('photo_size', models.CharField(choices=[('sm', 'small'), ('mid', 'medium'), ('big', 'big'), ('ori', 'original')], max_length=3)),
                ('browser', models.CharField(max_length=128)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user_agent_browser_family', models.CharField(max_length=32, null=True)),
                ('user_agent_browser_version', models.CharField(max_length=8, null=True)),
                ('user_agent_os_family', models.CharField(max_length=32, null=True)),
                ('user_agent_os_version', models.CharField(max_length=8, null=True)),
                ('user_agent_device_family', models.CharField(max_length=32, null=True)),
                ('user_agent_device_brand', models.CharField(max_length=32, null=True)),
                ('user_agent_device_model', models.CharField(max_length=32, null=True)),
                ('of_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.album')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.photo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhotoDownload',
            fields=[
                ('id', hashid_field.field.BigHashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', auto_created=True, min_length=13, prefix='', primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ip', models.GenericIPAddressField()),
                ('photo_size', models.CharField(choices=[('sm', 'small'), ('mid', 'medium'), ('big', 'big'), ('ori', 'original')], max_length=3)),
                ('browser', models.CharField(max_length=128)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user_agent_browser_family', models.CharField(max_length=32, null=True)),
                ('user_agent_browser_version', models.CharField(max_length=8, null=True)),
                ('user_agent_os_family', models.CharField(max_length=32, null=True)),
                ('user_agent_os_version', models.CharField(max_length=8, null=True)),
                ('user_agent_device_family', models.CharField(max_length=32, null=True)),
                ('user_agent_device_brand', models.CharField(max_length=32, null=True)),
                ('user_agent_device_model', models.CharField(max_length=32, null=True)),
                ('of_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.album')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.photo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
