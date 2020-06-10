# Generated by Django 3.0.5 on 2020-04-04 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200403_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='language',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='language',
            field=models.ForeignKey(help_text='Select language this book is written in', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Language'),
        ),
    ]