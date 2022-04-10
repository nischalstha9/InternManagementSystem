# Generated by Django 3.2 on 2022-04-10 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20220410_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.customuser')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
            ],
            options={
                'verbose_name_plural': 'Interns',
            },
            bases=('authentication.customuser',),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.IntegerField(blank=True, choices=[(0, 'Admin'), (1, 'Supervisor'), (2, 'Intern')], default=1, verbose_name='Role'),
        ),
    ]