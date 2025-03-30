from rest_framework import serializers
from .models import Equipe, Joueur, Match


class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nom', 'ville']

class JoueurSerializer(serializers.ModelSerializer):
    equipe_nom = serializers.CharField(source='equipe.nom', read_only=True)
    class Meta:
        model = Joueur
        fields = ['id', 'nom', 'poste', 'equipe', 'equipe_nom']


class MatchSerializer(serializers.ModelSerializer):
    equipe_domicile = serializers.StringRelatedField()
    equipe_exterieur = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = ['id_match', 'equipe_domicile', 'equipe_exterieur', 'buts_domicile', 'buts_exterieur']

    def create(self, validated_data):
        """Override create pour mettre à jour les stats des équipes après un match"""
        match = Match.objects.create(**validated_data)

        match.equipe_domicile.mettre_a_jour_stats()
        match.equipe_exterieur.mettre_a_jour_stats()

        return match


class EquipeSearchSerializer(serializers.Serializer):
    nom = serializers.CharField()
    ville = serializers.CharField()

class JoueurSearchSerializer(serializers.Serializer):
    nom = serializers.CharField()
    poste = serializers.CharField()
    equipe_nom = serializers.CharField()
    equipe_ville = serializers.CharField()
