# Generated by Django 5.1.4 on 2024-12-11 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ad_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='middle_name',
        ),
    ]
