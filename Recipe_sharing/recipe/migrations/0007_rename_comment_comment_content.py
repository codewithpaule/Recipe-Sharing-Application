# Generated by Django 5.0.3 on 2024-07-25 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_rename_content_comment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
    ]
