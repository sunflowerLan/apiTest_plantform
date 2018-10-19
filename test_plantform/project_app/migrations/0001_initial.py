# Generated by Django 2.1.1 on 2018-10-08 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectNumber_text', models.CharField(max_length=50)),
                ('projectName_text', models.CharField(max_length=200)),
                ('startDate', models.DateField()),
                ('projectManager_text', models.CharField(max_length=50)),
                ('projectDes_text', models.TextField(max_length=500)),
            ],
        ),
    ]