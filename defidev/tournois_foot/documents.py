from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Equipe, Joueur

# Définir un index Elasticsearch
equipe_index = Index('equipes')
joueur_index = Index('joueurs')

@registry.register_document
class EquipeDocument(Document):
    class Index:
        name = 'equipes'

    class Django:
        model = Equipe
        fields = ['nom', 'ville']

@registry.register_document
class JoueurDocument(Document):
    equipe_nom = fields.TextField(attr="equipe.nom")
    equipe_ville = fields.TextField(attr="equipe.ville")

    class Index:
        name = 'joueurs'

    class Django:
        model = Joueur
        fields = [
            'nom',
            'poste',
        ]