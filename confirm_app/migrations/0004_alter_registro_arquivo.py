# Generated by Django 4.2.6 on 2023-10-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirm_app', '0003_registro_extrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='arquivo',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
