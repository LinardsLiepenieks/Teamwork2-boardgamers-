# Generated by Django 4.2.7 on 2023-11-26 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardgame',
            old_name='creator',
            new_name='description',
        ),
    ]