# Generated by Django 4.2.9 on 2024-02-23 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_Sos', '0050_collaborateur_planifer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collaborateur',
            old_name='Planifer',
            new_name='Planifier',
        ),
    ]