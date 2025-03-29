from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, JoueurViewSet, equipe_liste, creer_equipe, joueur_liste, creer_joueur, creer_match, \
    classement, MatchViewSet, recherche, RechercheViewSet

# Création du routeur DRF
router = DefaultRouter()
router.register(r'equipes', EquipeViewSet)
router.register(r'joueurs', JoueurViewSet)
router.register(r'matchs', MatchViewSet)
router.register(r'recherche', RechercheViewSet, basename='recherche')

urlpatterns = [
    # Routes API
    path('api/', include(router.urls)),

    # Routes pour les équipes
    path('equipes/', equipe_liste, name='equipe_liste'),
    path('creer-equipe/', creer_equipe, name='creer_equipe'),

    # Routes pour les joueurs
    path('joueurs/', joueur_liste, name='joueur_liste'),
    path('creer-joueur/', creer_joueur, name='creer_joueur'),

    #Routes pour les matchs
    path("creer-matchs/", creer_match, name="creer_match"),
    path("classement/", classement, name="classement"),

    #Route pour l'API de recherche
    path('recherche/', recherche, name='recherche'),
]


