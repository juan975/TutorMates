from django.db import migrations, models
import django.db.models.deletion


def migrate_roles_to_role_model(apps, schema_editor):
    User = apps.get_model('tutoring', 'User')
    Role = apps.get_model('tutoring', 'Role')

    # Migrar los datos de roles del campo `role` de User al nuevo modelo Role
    for user in User.objects.all():
        if hasattr(user, 'role') and user.role:  # Verificar que el campo role existe y tiene datos
            Role.objects.create(user=user, role_type=user.role)


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0001_initial'),  # Reemplaza con la migración previa
    ]

    operations = [
        # Crear el modelo Role
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(choices=[
                    ('tutor', 'Tutor'),
                    ('estudiante', 'Estudiante'),
                    ('administrador', 'Administrador')],
                    max_length=15)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='role',
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # Migrar datos de roles al nuevo modelo Role
        migrations.RunPython(migrate_roles_to_role_model),
        # Eliminar el campo role del modelo User
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
