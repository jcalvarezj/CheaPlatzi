# Generated by Django 3.0.7 on 2020-07-20 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheaplatzi_deploy', '0002_auto_20200717_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.BigIntegerField(default=0),
        ),
    ]
