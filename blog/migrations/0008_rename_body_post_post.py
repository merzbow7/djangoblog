# Generated by Django 3.2.5 on 2021-07-16 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_body_comment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='post',
        ),
    ]