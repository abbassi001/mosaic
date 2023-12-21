# Generated by Django 3.2.18 on 2023-12-21 17:41

import authentication.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Cell')),
            ],
            options={
                'verbose_name': 'Cell',
                'verbose_name_plural': 'Cells',
                'db_table': 'cells',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='district')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'db_table': 'districts',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='province')),
            ],
            options={
                'verbose_name': 'province',
                'verbose_name_plural': 'provinces',
                'db_table': 'provinces',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Village')),
                ('cell', models.ForeignKey(db_column='cell', on_delete=django.db.models.deletion.CASCADE, to='authentication.cell', verbose_name='Cell')),
            ],
            options={
                'verbose_name': 'Village',
                'verbose_name_plural': 'Villages',
                'db_table': 'villages',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='sector')),
                ('district', models.ForeignKey(db_column='district', on_delete=django.db.models.deletion.CASCADE, to='authentication.district', verbose_name='District')),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'Sectors',
                'db_table': 'sectors',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(db_column='province', on_delete=django.db.models.deletion.CASCADE, to='authentication.province', verbose_name='Province'),
        ),
        migrations.AddField(
            model_name='cell',
            name='sector',
            field=models.ForeignKey(db_column='sector', on_delete=django.db.models.deletion.CASCADE, to='authentication.sector', verbose_name='Sectors'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=150, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can connect to this Dashboard.', verbose_name='Is Staff')),
                ('is_active', models.BooleanField(default=True, help_text='Indicates whether this user should be treated as active. Deselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
    ]
