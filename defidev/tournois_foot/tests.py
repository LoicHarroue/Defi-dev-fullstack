from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from .models import Equipe, Joueur, Match


# Create your tests here.

class EquipeJoueurTests(TestCase):

    def setUp(self):
        """Créer des données de test"""
        self.equipe = Equipe.objects.create(nom="PSG", ville="Paris")
        self.client = APIClient()  # Pour tester l’API REST

    def test_creer_equipe(self):
        """Vérifie que l'équipe est bien créée"""
        equipe = Equipe.objects.get(nom="PSG")
        self.assertEqual(equipe.ville, "Paris")

    def test_creer_joueur(self):
        """Vérifie qu'un joueur peut être créé et lié à une équipe"""
        joueur = Joueur.objects.create(nom="Mbappé", poste="Attaquant", equipe=self.equipe)
        self.assertEqual(joueur.equipe.nom, "PSG")
        self.assertEqual(joueur.poste, "Attaquant")

    def test_limite_joueurs_par_equipe(self):
        """Vérifie qu'on ne peut pas dépasser 11 joueurs par équipe"""
        for i in range(11):
            Joueur.objects.create(nom=f"Joueur {i}", poste="Milieu", equipe=self.equipe)

        with self.assertRaises(ValidationError):
            joueur_12 = Joueur(nom="Joueur 12", poste="Défenseur", equipe=self.equipe)
            joueur_12.clean()  # Doit lever une exception car il y a déjà 11 joueurs

    def test_api_liste_equipes(self):
        """Vérifie que l'API renvoie la liste des équipes"""
        response = self.client.get("/api/equipes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["nom"], "PSG")

    def test_api_creation_joueur(self):
        """Vérifie qu'on peut ajouter un joueur via l'API"""
        data = {"nom": "Neymar", "poste": "Attaquant", "equipe": self.equipe.id}
        response = self.client.post("/api/joueurs/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Joueur.objects.count(), 1)


class MatchTests(TestCase):

    def setUp(self):
        """Créer deux équipes et des matchs pour les tests"""
        self.equipe1 = Equipe.objects.create(nom="PSG", ville="Paris")
        self.equipe2 = Equipe.objects.create(nom="OM", ville="Marseille")

    def test_creation_match(self):
        """Vérifie que le match est bien enregistré"""
        match = Match.objects.create(equipe_domicile=self.equipe1, equipe_exterieur=self.equipe2, buts_domicile=2, buts_exterieur=1)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(match.buts_domicile, 2)

    def test_points_calcules_correctement(self):
        """Vérifie l'attribution correcte des points"""
        Match.objects.create(equipe_domicile=self.equipe1, equipe_exterieur=self.equipe2, buts_domicile=3, buts_exterieur=1)

        self.equipe1.mettre_a_jour_stats()
        self.equipe2.mettre_a_jour_stats()

        self.assertEqual(self.equipe1.points, 3)
        self.assertEqual(self.equipe2.points, 0)

    def test_match_unique(self):
        """Vérifie qu'un match entre deux équipes ne peut pas être joué deux fois"""
        Match.objects.create(equipe_domicile=self.equipe1, equipe_exterieur=self.equipe2, buts_domicile=1, buts_exterieur=1)

        with self.assertRaises(Exception):  # Vérifie qu'un 2ème match identique est refusé
            Match.objects.create(equipe_domicile=self.equipe1, equipe_exterieur=self.equipe2, buts_domicile=1, buts_exterieur=1)

