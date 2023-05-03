# Generated by Django 4.1.7 on 2023-05-03 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_remove_project_user_project_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='count_registred',
        ),
        migrations.RemoveField(
            model_name='project',
            name='sum_registred',
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0, verbose_name='оценка')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to='Accounts.project', verbose_name='Какой проект оценил')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Кто оценил')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'ordering': ['id'],
            },
        ),
    ]
