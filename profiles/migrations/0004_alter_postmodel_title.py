# Generated by Django 5.0.2 on 2024-03-18 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_postmodel_commentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
