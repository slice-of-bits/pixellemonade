# Generated by Django 4.1.7 on 2023-03-29 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prodigi', '0002_shoppingcard_shoppingcarditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcarditem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prodigi.product'),
        ),
    ]
