# Generated by Django 2.0.1 on 2018-04-07 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('add_content', '0014_auto_20180407_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='name',
            new_name='chapter_name',
        ),
        migrations.RenameField(
            model_name='usergroup',
            old_name='name',
            new_name='group_name',
        ),
    ]