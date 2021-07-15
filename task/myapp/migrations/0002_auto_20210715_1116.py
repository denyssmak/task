import django.contrib.auth.models
from django.db import migrations, models
def quiz_action(apps, schema_editor):
    Quiz = apps.get_model('myapp', 'Quiz')
    Quiz.objects.create(title='Python Test1',description='models1')
    Quiz.objects.create(title='Python Test2',description='models2')




class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial')
    ]

    operations = [
        migrations.RunPython(quiz_action, lambda x, y: None)
    ]