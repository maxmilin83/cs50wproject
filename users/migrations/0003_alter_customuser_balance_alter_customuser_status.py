# Generated by Django 5.0.4 on 2024-04-06 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_balance_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.PositiveIntegerField(default=5000),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('moderator', 'moderator'), ('regular', 'regular')], default='regular', max_length=100),
        ),
    ]
