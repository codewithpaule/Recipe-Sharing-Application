# Generated by Django 5.0.3 on 2024-07-24 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_step_recipe_delete_ingredient_delete_step'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
