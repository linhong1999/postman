# Generated by Django 3.0.7 on 2020-06-28 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.FileField(default='img/default.png', upload_to='img'),
        ),
    ]