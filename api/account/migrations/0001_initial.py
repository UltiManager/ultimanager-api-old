# Generated by Django 2.1 on 2018-09-06 13:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, help_text='A unique identifier for the user.', primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, help_text='A boolean indicating if the user should be allowed to perform actions on the site.', verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, help_text='A boolean indicating if the user is allowed to access the admin interface.', verbose_name='is staff')),
                ('is_superuser', models.BooleanField(default=False, help_text='A boolean indicating if the user should have all permissions without them being explicitly granted.', verbose_name='is superuser')),
                ('name', models.CharField(help_text='A name to publicly identify the user.', max_length=127, verbose_name='name')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time the user was created.', verbose_name='time created')),
                ('time_updated', models.DateTimeField(auto_now=True, help_text='The last time the user was edited.', verbose_name='time updated')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('time_created',),
            },
        ),
    ]
