from django.db import migrations


def quiz_action(apps, schema_editor):
    Quiz = apps.get_model('myapp', 'Quiz')
    Quiz.objects.create(title='Python Test1',description='models1')
    Quiz.objects.create(title='Python Test2',description='models2')




class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0003_auto_20201029_1352'),
    ]

    operations = [
        migrations.RunPython(quiz_action, lambda x, y: None)
    ]