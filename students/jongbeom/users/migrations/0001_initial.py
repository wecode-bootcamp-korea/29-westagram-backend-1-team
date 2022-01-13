# Generated by Django 4.0.1 on 2022-01-13 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=300, unique=True)),
                ('password', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]