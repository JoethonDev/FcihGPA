# Generated by Django 4.2.4 on 2024-06-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField()),
                ('student_name', models.CharField()),
                ('authorization', models.CharField()),
                ('gpa', models.FloatField()),
            ],
        ),
    ]
