# Generated by Django 4.2.9 on 2024-02-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_Sos', '0058_alter_collaborateur_activite_alter_collaborateur_csp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateur',
            name='Salaire_base',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]
