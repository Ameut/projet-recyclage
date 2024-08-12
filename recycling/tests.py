from django.test import TestCase, Client
from django.urls import reverse
from .models import PageIndex

class IndexViewTest(TestCase):

    def setUp(self):
        # Créez un client de test et des objets de test
        self.client = Client()
        self.url = reverse('index')

        # Créer un objet PageIndex pour le test
        self.page_index = PageIndex.objects.create(
            titre='Test Title',
            description='Test Description',
            image='images_index/test_image.jpg'
        )

    def test_index_view_status_code(self):
        # Teste si la page index est accessible
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        # Teste si la vue utilise le bon template
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_context_data(self):
        # Teste si les données contextuelles contiennent les informations correctes
        response = self.client.get(self.url)
        self.assertIn('page_index', response.context)
        self.assertEqual(response.context['page_index'][0], self.page_index)

from django.test import TestCase
from .models import Inventaire, Matiere

class InventaireTestCase(TestCase):
    def setUp(self):
        matiere = Matiere.objects.create(nom="Plastique", coefficient=1.2)
        Inventaire.objects.create(matiere=matiere, volume_m3=100)

    def test_inventaire_creation(self):
        inventaire = Inventaire.objects.get(matiere__nom="Plastique")
        self.assertEqual(inventaire.volume_m3, 100)
from django.test import TestCase
from .models import DemandeDevis, Localisation

class DevisTestCase(TestCase):
    def setUp(self):
        localisation = Localisation.objects.create(ville="Paris", adresse="123 Rue de Paris")
        DemandeDevis.objects.create(nom="Jean Dupont", email="jean@example.com", telephone="0123456789", message="Je voudrais un devis", localisation=localisation)

    def test_devis_creation(self):
        devis = DemandeDevis.objects.get(nom="Jean Dupont")
        self.assertEqual(devis.email, "jean@example.com")
from django.test import TestCase
from .models import DemandeDevis, Localisation

class DevisTestCase(TestCase):
    def setUp(self):
        localisation = Localisation.objects.create(ville="Paris", adresse="123 Rue de Paris")
        DemandeDevis.objects.create(nom="Jean Dupont", email="jean@example.com", telephone="0123456789", message="Je voudrais un devis", localisation=localisation)

    def test_devis_creation(self):
        devis = DemandeDevis.objects.get(nom="Jean Dupont")
        self.assertEqual(devis.email, "jean@example.com")
from django.test import TestCase
from .models import Contact, Localisation

class ContactTestCase(TestCase):
    def setUp(self):
        localisation = Localisation.objects.create(ville="Lyon", adresse="456 Rue de Lyon")
        Contact.objects.create(nom="Marie Dubois", email="marie@example.com", commentaires="Ceci est un commentaire", localisation=localisation)

    def test_contact_creation(self):
        contact = Contact.objects.get(nom="Marie Dubois")
        self.assertEqual(contact.commentaires, "Ceci est un commentaire")
