# Generated by Django 3.0.7 on 2020-06-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lyrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('lyrics', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='dummy',
        ),
    ]
