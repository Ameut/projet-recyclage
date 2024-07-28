from django.contrib import admin
from .models import PageIndex, PageEconomieCirculaire, Matiere, DemandeDevis, Temoin, Inventaire, Image, Localisation, InformationAgence, Contact, Balle

# Définir les classes Admin pour chaque modèle
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'date_contact')
    search_fields = ('nom', 'email')

@admin.register(PageIndex)
class PageIndexAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description')
    search_fields = ('titre',)

@admin.register(PageEconomieCirculaire)
class PageEconomieCirculaireAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description')
    search_fields = ('titre',)

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient')
    search_fields = ('nom',)

@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'date_demande')
    search_fields = ('nom', 'email')
    filter_horizontal = ('matieres',)

@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'note', 'date_soumission')
    search_fields = ('nom',)

@admin.register(Inventaire)
class InventaireAdmin(admin.ModelAdmin):
    list_display = ('matiere', 'volume_m3', 'date_enregistrement')
    search_fields = ('matiere__nom',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'fichier_image', 'page')
    search_fields = ('titre',)

@admin.register(Localisation)
class LocalisationAdmin(admin.ModelAdmin):
    list_display = ('ville', 'adresse')
    search_fields = ('ville',)

@admin.register(InformationAgence)
class InformationAgenceAdmin(admin.ModelAdmin):
    list_display = ('localisation', 'numero_telephone', 'email')
    search_fields = ('localisation__ville', 'numero_telephone')
    
@admin.register(Balle)
class BalleAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    
from .nosql_models import Material, Transaction

admin.site.register(Material)
admin.site.register(Transaction)

