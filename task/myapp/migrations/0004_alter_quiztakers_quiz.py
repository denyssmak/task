# Generated by Django 3.2.5 on 2021-07-15 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_quiztakers_correct_answers_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztakers',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_takers', to='myapp.quiz'),
        ),
    ]