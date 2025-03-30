from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Equipe(models.Model):
    nom = models.CharField(max_length=50)
    ville = models.CharField(max_length=100, default='Inconnu')
    buts_marques = models.PositiveIntegerField(default=0)
    buts_encaisses = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def mettre_a_jour_stats(self):
        """Calcule les stats après chaque match."""
        matchs_domicile = self.matchs_domicile.all()
        matchs_exterieur = self.matchs_exterieur.all()

        self.buts_marques = sum(m.buts_domicile for m in matchs_domicile if m.equipe_domicile == self)
        self.buts_marques += sum(m.buts_exterieur for m in matchs_exterieur if m.equipe_exterieur == self)

        self.buts_encaisses = sum(m.buts_exterieur for m in matchs_domicile if m.equipe_domicile == self)
        self.buts_encaisses += sum(m.buts_domicile for m in matchs_exterieur if m.equipe_exterieur == self)

        self.points = sum(m.resultat().get(self, 0) for m in matchs_domicile | matchs_exterieur)

        self.save()

    def __str__(self):
        return f"{self.nom} - {self.points} pts"


class Joueur(models.Model):
    POSTE_CHOICES = [
        ('Gardien', 'Gardien'),
        ('Défenseur', 'Défenseur'),
        ('Milieu', 'Milieu'),
        ('Attaquant', 'Attaquant'),
    ]

    nom = models.CharField(max_length=50)
    poste = models.CharField(choices=POSTE_CHOICES)
    equipe = models.ForeignKey(Equipe, related_name='joueurs', on_delete=models.CASCADE)

    def clean(self):
        """Validation pour limiter à 11 joueurs par équipe"""
        if self.equipe and Joueur.objects.filter(equipe=self.equipe).count() >= 11:
            raise ValidationError(f"L'équipe {self.equipe.nom} a déjà 11 joueurs.")

    def save(self, *args, **kwargs):
        """Appelle la validation avant de sauvegarder"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Match(models.Model):
    id_match = models.AutoField(primary_key=True)
    equipe_domicile = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="matchs_domicile", default='Inconnu')
    equipe_exterieur = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="matchs_exterieur", default='Inconnu')
    buts_domicile = models.PositiveIntegerField(default=0)
    buts_exterieur = models.PositiveIntegerField(default=0)

    def resultat(self):
        """Détermine le résultat du match et retourne les points attribués."""
        if self.buts_domicile > self.buts_exterieur:
            return {self.equipe_domicile: 3, self.equipe_exterieur: 0}
        elif self.buts_domicile < self.buts_exterieur:
            return {self.equipe_domicile: 0, self.equipe_exterieur: 3}
        else:
            return {self.equipe_domicile: 1, self.equipe_exterieur: 1}

    def __str__(self):
        return f"{self.equipe_domicile.nom} {self.buts_domicile} - {self.buts_exterieur} {self.equipe_exterieur.nom}"