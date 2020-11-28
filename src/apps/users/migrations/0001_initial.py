# Generated by Django 3.1.3 on 2020-11-28 13:01

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('safemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.safemodel')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(default='Имя', max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(default='Фамилия', max_length=100, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Отчество')),
                ('phone_number', models.CharField(default='', max_length=12, verbose_name='Номер телефона')),
                ('uuid', models.UUIDField(default=uuid.UUID('6c60be69-7b77-47d9-8f4f-e68fcc73f5ca'), editable=False)),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email пользователя')),
                ('status', models.IntegerField(choices=[(0, 'Главный администратор'), (1, 'Администратор'), (2, 'Пользователь'), (3, 'Ученик')], default=3, verbose_name='Тип учетной записи')),
                ('registration_reason', models.TextField(default='')),
                ('is_accepted', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'users',
                'ordering': ['last_name', 'first_name', 'middle_name'],
                'permissions': (('Редактирование пользователя', 'user_change'), ('Добавление пользователя', 'user_add'), ('Удаление пользователя', 'user_delete')),
            },
            bases=('core.safemodel', models.Model),
        ),
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('safemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.safemodel')),
                ('status', models.IntegerField(default=2, verbose_name='Статус одобрения')),
                ('registration_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_registration_request', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на регистрацию',
                'verbose_name_plural': 'Заявки на регистрацию',
                'db_table': 'registration_requests',
            },
            bases=('core.safemodel',),
        ),
    ]
