# Generated by Django 3.2.12 on 2024-04-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookedrooms', '0004_alter_bookedroom_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedroom',
            name='motif',
            field=models.CharField(default='aucun', max_length=100),
        ),
    ]
