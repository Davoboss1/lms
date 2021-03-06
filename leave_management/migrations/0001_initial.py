# Generated by Django 2.2.1 on 2019-12-27 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('School_Name', models.CharField(max_length=250)),
                ('School_Address', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Welfare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('phone_no', models.CharField(max_length=20)),
                ('Marital_Status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=10)),
                ('School', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave_management.School')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('phone_no', models.CharField(max_length=20)),
                ('Marital_Status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=10)),
                ('School', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management.School')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='leave_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(choices=[('1 week', '1 week'), ('2 weeks', '2 weeks'), ('3 weeks', '3 weeks'), ('1 month', '1 month'), ('2 months', '2 months'), ('3 months', '3 months'), ('6 months', '6 months')], max_length=20)),
                ('leave_type', models.CharField(choices=[('Emergency Leave', 'Emergency Leave'), ('Sickness Leave', 'Sickness Leave'), ('Maternity Leave', 'Maternity Leave'), ('Vacational Leave', 'Vacational Leave'), ('Annual Leave', 'Annual Leave')], max_length=50)),
                ('leave_message', models.CharField(blank=True, max_length=200, null=True)),
                ('leave_status', models.CharField(choices=[('Pending', 'Pending'), ('Declined', 'Declined'), ('Approved', 'Approved')], default='Pending', max_length=10)),
                ('is_hod_approved', models.BooleanField(default=False)),
                ('is_dean_approved', models.BooleanField(default=False)),
                ('is_welfare_approved', models.BooleanField(default=False)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management.Lecturer')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_leave', to='leave_management.School')),
            ],
        ),
        migrations.CreateModel(
            name='Head_of_Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('phone_no', models.CharField(max_length=20)),
                ('Marital_Status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=10)),
                ('School', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave_management.School')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('phone_no', models.CharField(max_length=20)),
                ('Marital_Status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=10)),
                ('School', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave_management.School')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
