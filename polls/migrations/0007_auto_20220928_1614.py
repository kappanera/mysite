# Generated by Django 3.2 on 2022-09-28 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20220928_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='info',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]