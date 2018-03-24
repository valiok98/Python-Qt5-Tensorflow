# Generated by Django 2.0.3 on 2018-03-22 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=25)),
                ('item_image', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('nick_name', models.CharField(max_length=20)),
                ('age', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.PersonalProfile'),
        ),
    ]
