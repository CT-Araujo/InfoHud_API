# Generated by Django 4.2.7 on 2023-12-21 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='oi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
            ],
        ),
    ]