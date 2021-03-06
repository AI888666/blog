# Generated by Django 2.2.16 on 2020-12-11 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('topic', '0002_auto_20201127_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='总余额')),
                ('order_id', models.IntegerField(verbose_name='打赏订单号')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有余额')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.Topic', verbose_name='打赏的文章')),
            ],
            options={
                'verbose_name': '总余额列表',
                'verbose_name_plural': '总余额列表',
            },
        ),
    ]
