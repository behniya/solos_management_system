# Generated by Django 5.1.4 on 2024-12-26 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='silolog',
            old_name='silo_id',
            new_name='silo',
        ),
        migrations.AlterField(
            model_name='silo',
            name='capacity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='silo',
            name='current_stock',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='silolog',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='silolog',
            name='change_type',
            field=models.CharField(choices=[('IN', 'Increase'), ('OUT', 'Decrease')], max_length=3),
        ),
    ]
