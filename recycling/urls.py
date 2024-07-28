
from .views import inventaires, supprimer_inventaire, telecharger_inventaires, information_agence

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('economie-circulaire/', views.economie_circulaire, name='economie_circulaire'),
    path('temoignages/', views.temoignages, name='temoignages'),
    path('inventaires/', views.inventaires, name='inventaires'),
    path('supprimer_inventaire/<int:id>/', views.supprimer_inventaire, name='supprimer_inventaire'),
    path('supprimer_balle/<int:id>/', views.supprimer_balle, name='supprimer_balle'),
    path('telecharger-inventaires-pdf/', views.telecharger_inventaires_pdf, name='telecharger_inventaires_pdf'),
    path('telecharger-inventaires/', views.telecharger_inventaires, name='telecharger_inventaires'),
    path('localisations/', views.localisations, name='localisations'),
    path('localisation/<int:localisation_id>/', views.information_agence, name='information_agence'),
    path('contact/', views.contact, name='contact'),
    path('demande-devis/', views.demande_devis, name='demande_devis'),
    path('information_agence/', information_agence, name='information_agence'),
    path('add_and_calculate/', views.add_and_calculate, name='add_and_calculate'),

]