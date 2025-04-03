# Generated by Django 5.2 on 2025-04-03 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='demandesuppressionobjet',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes_suppression', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='objetconnecte',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objets', to='objets.categorieobjet'),
        ),
        migrations.AddField(
            model_name='demandesuppressionobjet',
            name='objet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='objets.objetconnecte'),
        ),
        migrations.AddField(
            model_name='objetconnecte',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objets', to='objets.salle'),
        ),
        migrations.AddField(
            model_name='serviceconfiguration',
            name='objet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='configuration', to='objets.objetconnecte'),
        ),
    ]
