# Generated by Django 4.1.4 on 2023-07-10 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
