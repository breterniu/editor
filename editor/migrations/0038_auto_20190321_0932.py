# Generated by Django 2.0.13 on 2019-03-21 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0037_auto_20190320_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='ability_levels',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='access_rights',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='author',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='current_stamp',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='custom_theme',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='licence',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='examaccess',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='examaccess',
            name='user',
        ),
        migrations.RemoveField(
            model_name='examhighlight',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='examhighlight',
            name='picked_by',
        ),
        migrations.RemoveField(
            model_name='examquestion',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='examquestion',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='ability_levels',
        ),
        migrations.RemoveField(
            model_name='question',
            name='access_rights',
        ),
        migrations.RemoveField(
            model_name='question',
            name='author',
        ),
        migrations.RemoveField(
            model_name='question',
            name='copy_of',
        ),
        migrations.RemoveField(
            model_name='question',
            name='current_stamp',
        ),
        migrations.RemoveField(
            model_name='question',
            name='extensions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='licence',
        ),
        migrations.RemoveField(
            model_name='question',
            name='resources',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='question',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='questionaccess',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionaccess',
            name='user',
        ),
        migrations.RemoveField(
            model_name='questionhighlight',
            name='picked_by',
        ),
        migrations.RemoveField(
            model_name='questionhighlight',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionpullrequest',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='questionpullrequest',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='questionpullrequest',
            name='source',
        ),
        migrations.RemoveField(
            model_name='stampofapproval',
            name='object_content_type',
        ),
        migrations.RemoveField(
            model_name='stampofapproval',
            name='user',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='ExamAccess',
        ),
        migrations.DeleteModel(
            name='ExamHighlight',
        ),
        migrations.DeleteModel(
            name='ExamQuestion',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='QuestionAccess',
        ),
        migrations.DeleteModel(
            name='QuestionHighlight',
        ),
        migrations.DeleteModel(
            name='QuestionPullRequest',
        ),
        migrations.DeleteModel(
            name='StampOfApproval',
        ),
    ]
