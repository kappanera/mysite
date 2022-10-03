# Generated by Django 3.2 on 2022-09-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20220928_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='info',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
    ]
