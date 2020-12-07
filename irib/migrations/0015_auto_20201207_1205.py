# Generated by Django 3.1.3 on 2020-12-07 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irib', '0014_missingpos'),
    ]

    operations = [
        migrations.AddField(
            model_name='transition',
            name='prefixe',
            field=models.CharField(max_length=10, null=True, verbose_name='بادئة الكلمة'),
        ),
        migrations.AddField(
            model_name='transition',
            name='suffixe',
            field=models.CharField(max_length=10, null=True, verbose_name='لاحقة الكلمة'),
        ),
    ]