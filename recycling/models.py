from django.db import models
from django.utils import timezone

# Modèle pour la page d'accueil (index)
class PageIndex(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images_index/')

    def __str__(self):
        return self.titre

# Modèle pour la page économie circulaire
class PageEconomieCirculaire(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images_economie_circulaire/')

    def __str__(self):
        return self.titre

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.FloatField()
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Inventaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    volume_m3 = models.FloatField()
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventaire de {self.matiere.nom} ({self.date_enregistrement})"

class Balle(models.Model):
    nom = models.CharField(max_length=100)
    nombre = models.IntegerField(default=0, blank=True, null=True)
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE, related_name='balles')
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Balle {self.id} - {self.nom}'

# Modèle pour la localisation des agences
class Localisation(models.Model):
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)

    def __str__(self):
        return self.ville

class DemandeDevis(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    message = models.TextField()
    date_demande = models.DateTimeField(auto_now_add=True)
    matieres = models.ManyToManyField('Matiere')
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Devis de {self.nom} ({self.date_demande}) "



# Modèle pour les images
class Image(models.Model):
    titre = models.CharField(max_length=100)
    fichier_image = models.ImageField(upload_to='images/')
    page = models.ForeignKey(PageIndex, null=True, blank=True, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.titre

# Modèle pour les informations des agences
class InformationAgence(models.Model):
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Agence à {self.localisation.ville}"

# Modèle pour les contacts
class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    date_contact = models.DateTimeField(auto_now_add=True)
    commentaires = models.TextField(blank=True)
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nom
    
    
    
    
    
# Modèle pour les témoignages

class Temoin(models.Model):
    nom = models.CharField(max_length=100)
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Témoignage de {self.nom} ({self.note} étoiles)"