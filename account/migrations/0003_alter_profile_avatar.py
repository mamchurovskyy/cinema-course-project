# Generated by Django 3.2.16 on 2022-10-14 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d/'),
        ),
    ]
