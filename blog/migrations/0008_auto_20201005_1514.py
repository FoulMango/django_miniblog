# Generated by Django 3.1.1 on 2020-10-05 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201001_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='Blog posted on 2020-10-05', max_length=30),
        ),
    ]
