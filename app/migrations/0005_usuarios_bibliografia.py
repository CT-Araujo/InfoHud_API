# Generated by Django 4.2.7 on 2023-12-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_postagens_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='bibliografia',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
