from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.utils import formats
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
import csv
from reportlab.pdfgen import canvas

from .models import (
    PageIndex, PageEconomieCirculaire, DemandeDevis, Temoin, 
    Inventaire, Localisation, InformationAgence, Contact, 
    Matiere, Balle
)
from .forms import (
    ContactForm, InventaireForm, BalleForm, 
    DemandeDevisForm, TransactionForm
)


# ===================== Vues de page de base =====================

# Vue de la page d'accueil
def index(request):
    # Récupère tous les objets PageIndex de la base de données
    page_index = PageIndex.objects.all()
    # Affiche la page d'accueil avec les données de 'page_index'
    return render(request, 'index.html', {'page_index': page_index})

# Vue pour la page de l'économie circulaire
def economie_circulaire(request):
    # Récupère toutes les pages concernant l'économie circulaire
    page_economie = PageEconomieCirculaire.objects.all()
    # Affiche la page avec les données de 'page_economie'
    return render(request, 'economie_circulaire.html', {'pages': page_economie})

# ===================== Vue pour la demande de devis =====================

def demande_devis(request):
    # Vérifie si la requête est de type POST (soumission de formulaire)
    if request.method == 'POST':
        form = DemandeDevisForm(request.POST)# Si c'est un POST, on récupère les données du formulaire
        if form.is_valid():  # Vérifie si le formulaire est valide
            form.save()  # Sauvegarde les données du formulaire
            return JsonResponse({'success': True})  # Réponse JSON en cas de succès
        return JsonResponse({'success': False, 'errors': form.errors})  # Erreurs de validation en JSON
    else:
        form = DemandeDevisForm()  # Formulaire vide pour les requêtes GET
    # Affiche le formulaire de demande de devis
    return render(request, 'demande-devis.html', {'form': form})

# ===================== Authentification utilisateur =====================

def login_view(request):
    # Utilise la vue intégrée de connexion avec un template personnalisé
    return auth_views.LoginView.as_view(template_name='login.html')(request)


# ===================== Vues pour les inventaires =====================

# Décorateur pour exiger que l'utilisateur soit authentifié pour accéder à cette vue
@login_required  
def inventaires(request):
    # Instancie les formulaires d'inventaire et de balle pour les requêtes GET (initialement vides)
    form = InventaireForm()  # Formulaire pour ajouter un nouvel inventaire en vrac
    balle_form = BalleForm()  # Formulaire pour ajouter une balle liée à un inventaire
    error = None  # Variable pour stocker les messages d'erreur (utilisée si une sélection d'inventaire est manquante)

    # Vérifie si la requête est de type POST, ce qui signifie qu'un formulaire a été soumis
    if request.method == 'POST':  
        # Si le formulaire soumis est celui d'inventaire (repéré par 'volume_submit' dans les données de requête)
        if 'volume_submit' in request.POST:  # Si le formulaire soumis est celui d'inventaire (repéré par 'volume_submit' dans les données de requête)
            form = InventaireForm(request.POST)  # Remplit le formulaire d'inventaire avec les données POST
            if form.is_valid():  # Si le formulaire est valide (les champs requis sont remplis correctement)
                form.save()  # Sauvegarde l'inventaire dans la base de données
                return redirect('inventaires')  # Redirige vers la page des inventaires pour afficher les mises à jour

        # Si le formulaire soumis est celui de balle (repéré par 'balle_submit' dans les données de requête)
        elif 'balle_submit' in request.POST:  
            balle_form = BalleForm(request.POST)  # Remplit le formulaire de balle avec les données POST
            if balle_form.is_valid():  # Si le formulaire de balle est valide
                balle = balle_form.save(commit=False)  # Crée une instance de balle sans la sauvegarder tout de suite
                inventaire_id = request.POST.get('inventaire')  # Récupère l'ID de l'inventaire sélectionné
                if inventaire_id:  # Vérifie si un inventaire est sélectionné
                    balle.inventaire_id = inventaire_id  # Associe la balle à l'inventaire sélectionné
                    balle.save()  # Sauvegarde la balle dans la base de données
                else:
                    error = 'merci de selection une inventaire valide'  # Message d'erreur si aucun inventaire n'est sélectionné
                return redirect('inventaires')  # Redirige vers la page des inventaires

    # Récupère tous les inventaires et toutes les balles dans la base de données pour les afficher sur la page
    inventaires = Inventaire.objects.all()
    balles = Balle.objects.all()

    # Crée une liste de résultats pour chaque inventaire, avec des calculs pour afficher les informations clés
    resultats = [
        {
            'id': inventaire.id,
            'matiere': inventaire.matiere.nom,  # Nom de la matière de l'inventaire
            'volume': inventaire.volume_m3,  # Volume en m³ de l'inventaire
            'coef': inventaire.matiere.coefficient,  # Coefficient de la matière
            'resultat': inventaire.volume_m3 * inventaire.matiere.coefficient,  # Calcul du volume * coefficient
            'date': formats.date_format(inventaire.date_enregistrement, 'DATE_FORMAT')  # Date d'enregistrement formatée
        } for inventaire in inventaires  # Boucle sur chaque inventaire pour créer un dictionnaire de résultats
    ]

    # Rend la page 'inventaires.html' en y passant les formulaires, les inventaires, les balles, et les messages d'erreur
    return render(request, 'inventaires.html', {
        'form': form,  # Formulaire pour ajouter un inventaire
        'balle_form': balle_form,  # Formulaire pour ajouter une balle
        'resultats': resultats,  # Liste des résultats pour chaque inventaire
        'balles': balles,  # Liste de toutes les balles
        'error': error  # Message d'erreur éventuel
    })

# Vue pour supprimer un inventaire
def supprimer_inventaire(request, id):
    # Récupère l'inventaire ou renvoie une erreur 404 s'il n'existe pas
    inventaire = get_object_or_404(Inventaire, id=id)# Récupère l'inventaire ou renvoie une erreur 404 s'il n'existe pas
    inventaire.delete()  # Supprime l'inventaire
    return redirect('inventaires')

# Vue pour supprimer une balle
def supprimer_balle(request, id):
    balle = get_object_or_404(Balle, id=id)# Récupère la balle ou renvoie une erreur 404 s'il n'existe pas
    balle.delete()# Supprime la balle
    return redirect('inventaires')




# ===================== Téléchargement des inventaires =====================

# Téléchargement des inventaires au format CSV


def telecharger_inventaires(request):
    # Récupération de tous les inventaires
    inventaires = Inventaire.objects.all()
    
    # Création de la réponse HTTP avec un type de contenu CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventaires.csv"'
    
    # Initialisation de l'écriture CSV avec un délimiteur point-virgule
    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Écriture de l'en-tête du fichier CSV
    writer.writerow(['Matière', 'Volume (m³)', 'Balle', 'Coefficient', 'Résultat', 'Date d\'enregistrement'])
    
    # Parcourir chaque inventaire pour ajouter ses informations dans le fichier CSV
    for inventaire in inventaires:
        # Calcul du résultat (volume multiplié par le coefficient)
        resultat = inventaire.volume_m3 * inventaire.matiere.coefficient
        
        # Liste des balles associées pour cet inventaire
        balles = inventaire.balles.all()
        
        if balles:
            # Si des balles sont associées, créer une ligne pour chaque balle
            for balle in balles:
                writer.writerow([
                    inventaire.matiere.nom,                         # Nom de la matière
                    inventaire.volume_m3,                           # Volume en m³
                    balle.nom + f" (Nombre : {balle.nombre})",      # Nom et nombre de la balle
                    inventaire.matiere.coefficient,                 # Coefficient de la matière
                    resultat,                                       # Résultat du calcul (volume * coefficient)
                    formats.date_format(inventaire.date_enregistrement, "Y-m-d H:i:s")  # Date d'enregistrement formatée
                ])
        else:
            # Si aucune balle n'est associée, laisser la colonne "Balle" vide
            writer.writerow([
                inventaire.matiere.nom,                         # Nom de la matière
                inventaire.volume_m3,                           # Volume en m³
                "Aucune balle",                                 # Indique l'absence de balle
                inventaire.matiere.coefficient,                 # Coefficient de la matière
                resultat,                                       # Résultat du calcul (volume * coefficient)
                formats.date_format(inventaire.date_enregistrement, "Y-m-d H:i:s")  # Date d'enregistrement formatée
            ])
    
    # Retourne la réponse pour télécharger le fichier CSV
    return response


# Téléchargement des inventaires au format PDF
def telecharger_inventaires_pdf(request):
    inventaires = Inventaire.objects.all()
    response = HttpResponse(content_type='application/pdf')# Crée une réponse HTTP avec le type de contenu PDF
    response['Content-Disposition'] = 'attachment; filename=inventaires.pdf'#ajoute un en-tête pour le téléchargement du fichier
    p = canvas.Canvas(response)# Crée un objet Canvas pour générer le PDF
    p.drawString(100, 800, "Liste des Inventaires")

    y = 750
    for inventaire in inventaires:
        p.drawString(100, y, f"Matière: {inventaire.matiere.nom}")
        p.drawString(250, y, f"Volume (m³): {inventaire.volume_m3}")
        p.drawString(400, y, f"Date: {inventaire.date_enregistrement.strftime('%Y-%m-%d')}")
        y -= 20
        p.drawString(100, y, "Balles associées:")
        for balle in inventaire.balles.all():
            y -= 20
            p.drawString(120, y, f"- {balle.nom}: {balle.nombre}")
        y -= 40

    p.showPage()
    p.save()
    return response

# ===================== Vue de calcul des transactions CO2 =====================
from .utils import save_transaction, get_total_co2_saved, reset_transactions
def add_and_calculate(request):# Ajoute une transaction et calcule le CO2
    if request.method == 'POST':# Si la méthode est POST
        form = TransactionForm(request.POST)# Crée un formulaire de transaction avec les données de la requête POST
        if form.is_valid():
            # Réinitialise les transactions, enregistre la nouvelle transaction
            reset_transactions()
            save_transaction(
                form.cleaned_data['material'], # récupere le choix de utilisateur Nom de la matière (ex. "Papier", "Plastique")
                form.cleaned_data['quantity']
            )
            return redirect('add_and_calculate')
    else:
        form = TransactionForm()  # Formulaire vide pour GET
    total_co2_saved = get_total_co2_saved() # Récupère le total de CO2 économisé
    # Rend la page avec le total de CO2 économisé
    return render(request, 'add_and_calculate.html', {'form': form, 'total_co2_saved': total_co2_saved})# Rend la page avec le total de CO2 économisé


# ===================== Vue de contact =====================

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde du formulaire de contact
            return JsonResponse({'message': 'Form submitted successfully'})
        return JsonResponse({'message': 'Form submission failed', 'errors': form.errors})
    else:
        form = ContactForm()  # Formulaire vide pour requêtes GET
    return render(request, 'contact.html', {'form': form})


# ===================== Vues de localisations et informations d'agence =====================

def localisations(request):
    # Récupère toutes les localisations
    localisations = Localisation.objects.all()
    # Rend la page des localisations
    return render(request, 'localisations.html', {'localisations': localisations})

def information_agence(request, localisation_id):
    # Récupère une localisation spécifique et les informations associées
    localisation = get_object_or_404(Localisation, id=localisation_id)
    infos = InformationAgence.objects.filter(localisation=localisation)
    # Rend la page d'informations d'agence avec les détails
    return render(request, 'information_agence.html', {'infos': infos, 'localisation': localisation})

# logger de sécurité
"""from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging
import os 

# Instanciation du logger
logger = logging.getLogger('security')

@login_required
def secure_view(request):
    # Log l'accès à la page sécurisée
    logger.info(f"Utilisateur connecté : {request.user.username}")

    # Chemin vers le fichier de logs
    log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'security.log')
    logs = []

    # Lecture des logs si le fichier existe
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()

    return render(request, 'secure_page.html', {'logs': logs})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Authentification Django

        if user is not None:
            login(request, user)  # Connexion de l'utilisateur
            logger.info(f"Connexion réussie pour : {username}")
            return redirect('secure_view')  # Redirige vers la page sécurisée
        else:
            logger.warning(f"Tentative de connexion échouée pour : {username}")
            return render(request, 'login_view.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect.'})
    
    return render(request, 'login_view.html')  # Affiche la page de connexion"""""
