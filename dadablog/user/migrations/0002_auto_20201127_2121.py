# Generated by Django 2.2.16 on 2020-11-27 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户列表', 'verbose_name_plural': '用户列表'},
        ),
    ]