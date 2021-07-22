from django.db import migrations


def quiz_action(apps, schema_editor):
    Question = apps.get_model('myapp', 'Question')
    Quiz = apps.get_model('myapp', 'Quiz')

    quiz1 = Quiz.objects.create(title='Python Test1', description='quiz1')
    Question.objects.create(
        quiz=quiz1, 
        title_anwers='200 is 200',
        response1='Undefined',
        response2='True',
        correct2=True,
        response3='None',
        response4='False',
    )
    Question.objects.create(
        quiz=quiz1, 
        title_anwers='raise',
        response1='ValueError',
        response2='SyntaxError',
        response3='RuntimeError',
        correct3=True,
        response4='TypeError',
    )
    Question.objects.create(
        quiz=quiz1, 
        title_anwers='5 * 3',
        response1='16',
        response2='17',
        response3='18',
        response4='15',
        correct4=True,
    )
    Question.objects.create(
        quiz=quiz1, 
        title_anwers='120 + 40',
        response1='160',
        correct1=True,
        response2='180',
        response3='170',
        response4='200',
    ) 
    Question.objects.create(
        quiz=quiz1, 
        title_anwers='[1, 3] + [3, 1]',
        response1='[1, 3]',
        response2='TypeError',
        response3='[1, 3, 3, 1]',
        correct3=True,
        response4='[3, 1]',
    )

    quiz2 = Quiz.objects.create(title='Python Test2', description='quiz2')
    Question.objects.create(
        quiz=quiz2, 
        title_anwers='300 is 300',
        response1='Undefined',
        response2='True',
        response3='None',
        response4='False',
        correct4=True,
    )
    Question.objects.create(
        quiz=quiz2, 
        title_anwers='11 * 11',
        response1='111',
        response2='110',
        response3='122',
        response4='121',
        correct4=True,
    )
    Question.objects.create(
        quiz=quiz2, 
        title_anwers='Сколько библиотек можно импортировать в один проект?',
        response1='10',
        response2='100',
        response3='9',
        response4='Неограниченное количество',
        correct4=True,
    )
    Question.objects.create(
        quiz=quiz2, 
        title_anwers='7 - 6',
        response1='2',
        response2='1',
        correct2=True,
        response3='3',
        response4='-1',
    ) 
    Question.objects.create(
        quiz=quiz2, 
        title_anwers='pip',
        response1='pip',
        response2='python',
        response3='Python Installer Package',
        correct3=True,
        response4='--',
    )



class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(quiz_action, lambda x, y: None)
    ]