# Generated by Django 3.1.7 on 2021-03-22 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_content_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='categories',
        ),
        migrations.AddField(
            model_name='content',
            name='categories',
            field=models.CharField(blank=True, choices=[('test1', 'test1'), ('test2', 'test2')], max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
    ]
