# Generated by Django 2.1.7 on 2019-04-24 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs_app', '0003_auto_20190424_1003'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='song',
            unique_together={('artist', 'song')},
        ),
    ]