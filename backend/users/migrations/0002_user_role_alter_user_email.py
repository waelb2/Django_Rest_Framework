# Generated by Django 5.0 on 2024-12-06 20:25

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('saleman', 'Saleman'), ('buyer', 'Buyer')], default=users.models.UserRole['BUYER'], max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
