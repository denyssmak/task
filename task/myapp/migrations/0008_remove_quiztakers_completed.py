# Generated by Django 3.2.5 on 2021-07-18 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_quiztakers_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiztakers',
            name='completed',
        ),
    ]