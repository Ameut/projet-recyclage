from django import forms
from .models import PageIndex, PageEconomieCirculaire, Matiere, DemandeDevis, Temoin, Inventaire, Image, Localisation, InformationAgence, Contact, Balle

class PageIndexForm(forms.ModelForm):
    class Meta:
        model = PageIndex
        fields = ['titre', 'description', 'image']

class PageEconomieCirculaireForm(forms.ModelForm):
    class Meta:
        model = PageEconomieCirculaire
        fields = ['titre', 'description', 'image']

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'coefficient']

class DemandeDevisForm(forms.ModelForm):
    class Meta:
        model = DemandeDevis
        fields = ['nom', 'email', 'telephone', 'message', 'matieres']

class TemoinForm(forms.ModelForm):
    class Meta:
        model = Temoin
        fields = ['nom', 'note', 'commentaire']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['titre', 'fichier_image', 'page']

class LocalisationForm(forms.ModelForm):
    class Meta:
        model = Localisation
        fields = ['ville', 'adresse']

class InformationAgenceForm(forms.ModelForm):
    class Meta:
        model = InformationAgence
        fields = ['localisation', 'numero_telephone', 'email']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'commentaires']

class InventaireForm(forms.ModelForm):
    class Meta:
        model = Inventaire
        fields = ['matiere', 'volume_m3']

class BalleForm(forms.ModelForm):
    class Meta:
        model = Balle
        fields = ['nom', 'nombre', 'inventaire']
        
class DemandeDevisForm(forms.ModelForm):
    class Meta:
        model = DemandeDevis
        fields = ['nom', 'email', 'telephone', 'message', 'matieres', 'localisation']

    localisation = forms.ModelChoiceField(queryset=Localisation.objects.all(), empty_label="Sélectionnez une localisation")
    
    
from django import forms
from django.conf import settings

class TransactionForm(forms.Form):
    # Champ de sélection pour les matériaux, initialement vide
    material = forms.ChoiceField(choices=[])
    # Champ pour entrer la quantité de matériau
    quantity = forms.FloatField()

    # On surcharge la méthode __init__ pour modifier les choix du champ 'material'
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Met à jour les choix disponibles pour le champ 'material'
        self.fields['material'].choices = self.get_material_choices()

    # Méthode pour récupérer les choix des matériaux depuis la base de données MongoDB
    def get_material_choices(self):
        # Accéder à la base de données MongoDB via les paramètres de configuration de Django
        db = settings.MONGO_DB
        # Récupérer tous les matériaux de la collection 'material'
        materials = db.material.find()
        # Créer une liste de tuples (nom, nom) pour les choix du champ 'material'
        choices = [(material['name'], material['name']) for material in materials]
        return choices  # Retourner la liste de choix