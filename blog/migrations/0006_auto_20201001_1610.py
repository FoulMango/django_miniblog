# Generated by Django 3.1.1 on 2020-10-01 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201001_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['creation_date'], 'permissions': (('can_publish', 'Can publish new blog posts'),)},
        ),
    ]