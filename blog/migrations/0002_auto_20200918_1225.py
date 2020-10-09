# Generated by Django 3.1.1 on 2020-09-18 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['creation_date']},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='Blog posted on 2020-09-18', max_length=30),
        ),
    ]
