from django import forms
from .models import Equipe, Joueur, Match


class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom', 'ville']

class JoueurForm(forms.ModelForm):
    class Meta:
        model = Joueur
        fields = ['nom', 'poste', 'equipe']
        widgets = {
            'poste': forms.Select(choices=Joueur.POSTE_CHOICES, attrs={'class': 'form-control'}),
            'equipe': forms.Select(attrs={'class': 'form-control'}),
        }

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match  # Spécifie le modèle 'Match'
        fields = ['equipe_domicile', 'equipe_exterieur', 'buts_domicile', 'buts_exterieur']

