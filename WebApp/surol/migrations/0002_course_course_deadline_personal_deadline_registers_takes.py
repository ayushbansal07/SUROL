# Generated by Django 2.0.3 on 2018-03-19 04:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('dept_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course_deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=500)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Personal_deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('comments', models.CharField(max_length=500)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Registers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Course')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surol.Professor')),
            ],
        ),
    ]