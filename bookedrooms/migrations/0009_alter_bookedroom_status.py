# Generated by Django 3.2.12 on 2024-05-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookedrooms', '0008_auto_20240503_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedroom',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('canceled', 'Annulé'), ('validated', 'Validé')], default='pending', max_length=100),
        ),
    ]
