# Generated by Django 3.1.3 on 2020-11-24 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irib', '0004_auto_20201124_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='from_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_transitions', to='irib.state', verbose_name='Etat de provenance'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='to_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prev_transitions', to='irib.state', verbose_name='Etat de destination'),
        ),
    ]
