from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from .models import Equipe, Joueur, Match
from .serializers import EquipeSerializer, JoueurSerializer, MatchSerializer, JoueurSearchSerializer, \
    EquipeSearchSerializer
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import EquipeForm, JoueurForm, MatchForm
from django_elasticsearch_dsl.search import Search
from .documents import EquipeDocument, JoueurDocument
from elasticsearch_dsl import Q

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class JoueurViewSet(viewsets.ModelViewSet):
    queryset = Joueur.objects.all()
    serializer_class = JoueurSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class RechercheViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.GET.get('q', '')
        results = {'equipes': [], 'joueurs': []}

        if query:
            # Recherche dans les équipes
            search_equipes = Search(index='equipes').query('match', nom=query)
            equipes = [hit.to_dict() for hit in search_equipes.execute()]
            results['equipes'] = EquipeSearchSerializer(equipes, many=True).data

            # Recherche dans les joueurs (nom ou poste)
            search_joueurs = Search(index='joueurs').query(
                Q("bool", should=[
                    Q("match", nom=query),
                    Q("match", poste=query)
                ])
            )

            joueurs = [hit.to_dict() for hit in search_joueurs.execute()]
            results['joueurs'] = JoueurSearchSerializer(joueurs, many=True).data

        return Response(results)

def creer_equipe(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipe_liste')
    else:
        form = EquipeForm()
    return render(request, 'creer_equipe.html', {'form': form})

def equipe_liste(request):
    equipes = Equipe.objects.all()
    return render(request, 'equipe_liste.html', {'equipes': equipes})

def creer_joueur(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('joueur_liste')
    else:
        form = JoueurForm()
    return render(request, 'creer_joueur.html', {'form': form})

def joueur_liste(request):
    joueurs = Joueur.objects.all()
    return render(request, 'joueur_liste.html', {'joueurs': joueurs})


def creer_match(request):
    """Affiche le formulaire et ajoute un match"""
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()

            # Mise à jour des statistiques des équipes après chaque match
            match.equipe_domicile.mettre_a_jour_stats()
            match.equipe_exterieur.mettre_a_jour_stats()

            return redirect("classement")
    else:
        form = MatchForm()

    return render(request, "creer_match.html", {"form": form})

def classement(request):
    """Affiche le classement des équipes, trié par points puis buts marqués"""
    equipes = Equipe.objects.all().order_by("-points", "-buts_marques")
    return render(request, "classement.html", {"equipes": equipes})

def recherche(request):
    query = request.GET.get('q', '')
    results = {'equipes': [], 'joueurs': []}

    if query:
        # Recherche dans les équipes
        search_equipes = Search(index='equipes').query('match', nom=query)
        equipes = [hit.to_dict() for hit in search_equipes.execute()]
        results['equipes'] = equipes

        # Recherche dans les joueurs (nom ou poste)
        search_joueurs = Search(index='joueurs').query(
            Q("bool", should=[
                Q("match", nom=query),
                Q("match", poste=query),
                Q("match", equipe_nom=query)
            ])
        )
        joueurs = [hit.to_dict() for hit in search_joueurs.execute()]
        results['joueurs'] = joueurs

    return render(request, 'recherche.html', {'results': results, 'query': query})