# Generated by Django 4.2.9 on 2024-02-28 10:00

import admin_Sos.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_Sos', '0059_alter_collaborateur_salaire_base'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Salaire',
            new_name='Salaire_CANADA',
        ),
        migrations.CreateModel(
            name='Salaire_FRANCE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_de_salaire', admin_Sos.models.MonthYearField(blank=True, max_length=7, null=True)),
                ('salaire_finale', models.IntegerField(blank=True, default=0, null=True)),
                ('id_Collaborateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_Sos.collaborateur')),
            ],
        ),
    ]