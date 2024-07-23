from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import PageIndex, PageEconomieCirculaire, DemandeDevis, Temoin, Inventaire, Localisation, InformationAgence, Contact, Matiere, Balle
from .forms import ContactForm, InventaireForm, BalleForm, DemandeDevisForm
from django.http import JsonResponse
import csv
from django.http import HttpResponse
from django.utils import formats
from django.utils import formats  # Import pour la gestion des formats de date
from django.http import HttpResponse


# Vue pour afficher la page d'accueil
def index(request):
    page_index = PageIndex.objects.all()
    return render(request, 'index.html', {'page_index': page_index})

# Vue pour afficher la page sur l'économie circulaire
def economie_circulaire(request):
    page_economie = PageEconomieCirculaire.objects.all()
    return render(request, 'economie_circulaire.html', {'pages': page_economie})

# Vue pour afficher les demandes de devis
def demande_devis(request):
    if request.method == "POST":
        form = DemandeDevisForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('success_page')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
    else:
        form = DemandeDevisForm()
    return render(request, 'demande_devis.html', {'form': form})

from .models import Temoin
from .forms import TemoinForm
# Vue pour afficher les témoignages
def temoignages(request):
    if request.method == "POST":
        form = TemoinForm(request.POST)
        if form.is_valid():
            form.save()  #    Sauvegarde du formulaire dans la base de données
    else:
        form = TemoinForm()  # Création d'une instance de formulaire vide
    temoignages = Temoin.objects.all()  # Fetch all testimonials from the database
    return render(request, 'index.html', {'form': form, 'temoignages': temoignages})
from django.shortcuts import render, redirect
from .forms import InventaireForm, BalleForm
from .models import Inventaire, Balle
from django.utils import formats

def inventaires(request):
    form = InventaireForm()
    balle_form = BalleForm()
    error = None

    if request.method == 'POST':
        if 'volume_submit' in request.POST:
            form = InventaireForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('inventaires')
        elif 'balle_submit' in request.POST:
            balle_form = BalleForm(request.POST)
            if balle_form.is_valid():
                balle = balle_form.save(commit=False)
                inventaire_id = request.POST.get('inventaire')
                if inventaire_id:
                    balle.inventaire_id = inventaire_id
                    balle.save()
                else:
                    error = 'Please select a valid Inventaire'
                return redirect('inventaires')

    inventaires = Inventaire.objects.all()
    balles = Balle.objects.all()

    resultats = []
    for inventaire in inventaires:
        resultat = inventaire.volume_m3 * inventaire.matiere.coefficient
        resultats.append({
            'id': inventaire.id,
            'matiere': inventaire.matiere.nom,
            'volume': inventaire.volume_m3,
            'coef': inventaire.matiere.coefficient,
            'resultat': resultat,
            'date': formats.date_format(inventaire.date_enregistrement, 'DATE_FORMAT')
        })

    return render(request, 'inventaires.html', {
        'form': form,
        'balle_form': balle_form,
        'resultats': resultats,
        'balles': balles,
        'error': error
    })

def supprimer_inventaire(request, id):
    inventaire = get_object_or_404(Inventaire, id=id)
    inventaire.delete()
    return redirect('inventaires')

def supprimer_balle(request, id):
    balle = get_object_or_404(Balle, id=id)
    balle.delete()
    return redirect('inventaires')
# Vue pour afficher les localisations
def localisations(request):
    localisations = Localisation.objects.all()
    return render(request, 'localisations.html', {'localisations': localisations})

# Vue pour afficher les informations d'une agence spécifique
def information_agence(request, localisation_id):
    localisation = get_object_or_404(Localisation, id=localisation_id)
    infos = InformationAgence.objects.filter(localisation=localisation)
    return render(request, 'information_agence.html', {'infos': infos, 'localisation': localisation})

# Vue pour gérer le formulaire de contact
from django.http import JsonResponse

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #  Sauvegarde du formulaire dans la base de données
            return JsonResponse({'message': 'Form submitted successfully'})# Retourne un message JSON en cas de succès
    else:
        form = ContactForm()  # Create a new instance of the form for GET requests

    return render(request, 'contact.html', {'form': form})

def telecharger_inventaires(request):# Vue pour télécharger les inventaires au format CSV
    inventaires = Inventaire.objects.all()
    
    # Configuration de la réponse HTTP pour le téléchargement CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventaires.csv"'
    
    # Écriture des en-têtes CSV
    writer = csv.writer(response)
    writer.writerow(['Matière', 'Volume (m³)', 'Coefficient', 'Résultat', 'Date d\'enregistrement', 'Nombre de Balles'])
    
    # Écriture des lignes de données pour chaque inventaire
    for inventaire in inventaires:
        balles_info = '\n'.join([f"{balle.nom}: {balle.nombre}" for balle in inventaire.balles.all()])
        writer.writerow([
            inventaire.matiere.nom,
            inventaire.volume_m3,
            inventaire.matiere.coefficient,
            inventaire.volume_m3 * inventaire.matiere.coefficient,
            formats.date_format(inventaire.date_enregistrement, "DATETIME_FORMAT"),  # Formatage de la date en français
            balles_info
        ])
    
    return response

from reportlab.pdfgen import canvas
from .models import Inventaire

# Vue pour télécharger les inventaires au format PDF
def telecharger_inventaires_pdf(request):# Vue pour télécharger les inventaires au format PDF
    inventaires = Inventaire.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=inventaires.pdf'

    p = canvas.Canvas(response)# configuration  variables       
    p.drawString(100, 800, "Liste des Inventaires")

    y = 750
    for inventaire in inventaires:
        p.drawString(100, y, f"Matière: {inventaire.matiere.nom}")
        p.drawString(250, y, f"Volume (m³): {inventaire.volume_m3}")
        p.drawString(400, y, f"Date: {inventaire.date_enregistrement.strftime('%Y-%m-%d')}")

        y -= 20 #  Décalage de la ligne suivante
        p.drawString(100, y, "Balles associées:")# Affichage des balles associées à l'inventaire
        for balle in inventaire.balles.all():
            y -= 20
            p.drawString(120, y, f"- {balle.nom}: {balle.nombre}")#   Affichage des balles associées à l'inventaire

        y -= 40

    p.showPage()
    p.save()

    return response


def recuperer_balles(request):
    balles = Balle.objects.all()
    return render(request, 'balles.html', {'balles': balles})


