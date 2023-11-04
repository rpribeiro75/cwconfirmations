# Generated by Django 4.2.1 on 2023-11-03 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confirm_app', '0005_alter_registro_arquivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=50)),
                ('referencia', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='registro',
            name='engagement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='confirm_app.engagement'),
            preserve_default=False,
        ),
    ]
