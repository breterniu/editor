# Generated by Django 2.0.5 on 2018-07-25 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0034_set_contributors'),
    ]

    operations = [
        migrations.AddField(
            model_name='customparttype',
            name='extensions',
            field=models.ManyToManyField(blank=True, to='editor.Extension'),
        ),
    ]
