# Generated by Django 3.2 on 2022-09-25 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
