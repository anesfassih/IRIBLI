# Generated by Django 3.1.3 on 2020-11-24 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irib', '0005_auto_20201124_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='halat_al_irab',
            field=models.CharField(choices=[('raf3', 'رفع'), ('nasb', 'نصب'), ('jarr', 'جر'), ('jazm', 'جزم'), ('unspec', 'unspec')], max_length=20, null=True, verbose_name='حالة الإعراب'),
        ),
    ]
