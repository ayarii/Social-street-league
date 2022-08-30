from difflib import context_diff
from django.shortcuts import render, redirect
from .models import Event
from post.models import Post
from django.core.paginator import Paginator
from .forms import EventForm
# Create your views here.

#def Display(request):
    #return render(request,'event.html' ,{'ev' : Event.objects.all()} )
import numpy as np
def cosij(ui,uj):
    """
    retourne le resultat du calcul de s_ij pour 2 valeurs ui(i) et uj(j)
    paramètres :
    les vecteurs ui et uj de modules mod(ui) et mod(uj)
    """
    s=0
    for i in range(len(ui)):
        s += ui[i]*uj[i]/(mod(ui)*mod(uj))
    return s

def mod(u):
    """
    calcule le module du vecteur mis en paramètre
    """
    s=0
    for i in range(len(u)):
        s += u[i]*u[i]
    s = s**0.5
    return s

def matrice_cos(A,B):
    """
    retourne la matrice de similitude entre 2 listes 
    de dimension 2 (liste de liste), A et B mises en paramètre
    """
    C = np.zeros(shape=(len(A),len(B)))
    for i in range(len(A)):
        for j in range(len(B)):
            C[i,j]=cosij(A[i],B[j])
    return C

import re
def decoupe(texte):
    
    texte_decoupe = list(re.split('; |, |\' |\n |\s+',texte))
    texte_mini=[]
    for t in texte_decoupe:
        match = re.match('[a-z]{4,}',t)
        if match!=None:
            texte_mini.append(match.group(0))
    return texte_mini
import pandas as pd
df = pd.read_csv("descriptif.csv", sep=";")
def mots(descriptif):
    """
    retourne la liste de tous les mots de descriptif, de manière unique, dans une seule liste
    """
    liste_de_mots = []
    for desc in descriptif:
        for i in desc : 
            if not(i in liste_de_mots):
                liste_de_mots.append(i)
    return liste_de_mots
def tab(descriptif):
    """
    retourne la liste tableau avec les occurences pour chaque article (chaque rang) 
    des mots retenus (mots)
    une colonne par mot
    """
    tableau = []
    mots_elements = mots(descriptif)
    for desc in descriptif:
        ligne = []
        nombre_de_mots = len(desc)
        ligne = [desc.count(mot)/nombre_de_mots for mot in mots_elements]
        tableau.append(ligne)
    return tableau
def articles(tab):
    tab=tab.sort_values(ascending=False)
    articles = list(tab.index.values)
    recom = 'l\'article \033[1m {0:15} \033[0;0m est similaire à \033[1m{1:15}\033[0;0m voire peut être un peu à \033[1m{2:15}\033[0;0m'.format(articles[0],articles[1],articles[2])
    redd='{0:15}'.format(articles[1])
    return articles[1]

def recommandation(dataf):
    texte=[]
    col = list(dataf.keys()) 
    for c in col:
        if c== "info" :
          tab_red=[]
          tab_red = dataf[c]
          texte.append(articles(tab_red))
    return texte
def recommandationf(request):
    post_list=Post.objects.all()
    name=""
    for p in post_list :
        if p.user.username==request.user.username :
            name=p.post_description
    
    df.at[0,"info"]=name
    col = list(df.keys())
# on créé une liste (descriptif) contenant, pour chaque article, une liste avec TOUS les mots retenus dans la description
    descriptif = []
    for cle in col:
        desc = df[cle][0]
        descriptif.append(decoupe(desc))
    tableau = tab(descriptif)
    df2=pd.DataFrame(tableau,index=col,columns=mots(descriptif))
    mat=matrice_cos(tableau,tableau)
    df3=pd.DataFrame(mat,index=col,columns=col)
    texte = recommandation(df3)
    for t in texte:
      name=t
    return name

def addev(request):

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if  form.is_valid():
            form.save()
            return redirect ('/addev?submitted=True')
        else:
            context = {
                'form': EventForm,
            }
        return render(request,'addev.html',context)
    context = {
                'form': EventForm,
            }
    return render(request,'addev.html',context)

def list_event(request):
    event_list = Event.objects.all()
    id=100
    name=""
    post_list=Post.objects.all()
    x=""
    for p in post_list :
        if p.user.username==request.user.username :
            x=p.post_description
    p = Paginator(event_list, 3)
    page = request.GET.get('page')
    events = p.get_page(page)
    nums = "a" * events.paginator.num_pages
    if request.user.username != "" :
       if x!= ""   : 
         name =recommandationf(request)
    name1="takwira"
    
    for p in event_list :
        if p.title_event==name :
            id=p.id
    
    context = {'event_list': event_list,
    'events': events,
    'nums': nums,
    'kk': name,
     'idd' :id }
    return render(request,'event.html',context
     )

def even(request, id):
    obj = Event.objects.get(id = id)
    context = {
        #'title': obj.title_event,
        #'descrition ': obj.description_event,
        #'image': obj.image,
        #'location': obj.location_event,
        #'date': obj.date_event,
        #'Activity': obj.Activity_event

        'object': obj
    }
    return render(request,'even.html', context
     )
