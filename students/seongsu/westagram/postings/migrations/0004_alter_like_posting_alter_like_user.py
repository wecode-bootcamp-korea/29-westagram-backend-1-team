# Generated by Django 4.0.1 on 2022-01-19 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_password'),
        ('postings', '0003_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postinglike', to='postings.posting'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userlike', to='users.user'),
        ),
    ]