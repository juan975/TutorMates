# Generated by Django 5.1.4 on 2025-01-22 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0003_alter_user_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='tutorias', to='tutoring.rol'),
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('tutoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='tutoring.tutoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'tutoria')},
            },
        ),
    ]
