# Generated by Django 3.2.12 on 2022-03-05 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20220305_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, help_text='chapter or specific title related to this file ', max_length=369, null=True),
        ),
        migrations.AlterField(
            model_name='lecturebook',
            name='title',
            field=models.CharField(blank=True, help_text='chapter or specific title related to this file ', max_length=369, null=True),
        ),
        migrations.AlterField(
            model_name='lecturepdf',
            name='title',
            field=models.CharField(blank=True, help_text='chapter or specific title related to this file ', max_length=369, null=True),
        ),
        migrations.AlterField(
            model_name='lectureppt',
            name='title',
            field=models.CharField(blank=True, help_text='chapter or specific title related to this file ', max_length=369, null=True),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
