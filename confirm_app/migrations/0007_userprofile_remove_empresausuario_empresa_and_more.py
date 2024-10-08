# Generated by Django 4.2.6 on 2024-09-17 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('confirm_app', '0006_usuariocomempresa_empresausuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('cargo', models.CharField(blank=True, max_length=100)),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='confirm_app.empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='empresausuario',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='empresausuario',
            name='user',
        ),
        migrations.DeleteModel(
            name='UsuarioComEmpresa',
        ),
        migrations.DeleteModel(
            name='EmpresaUsuario',
        ),
    ]
