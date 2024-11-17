import datetime
from django.conf import settings

# Fonction pour sauvegarder une transaction de recyclage dans MongoDB
def save_transaction(material_name, quantity):
    # Accéder à la base de données MongoDB via les paramètres de configuration de Django
    db = settings.MONGO_DB
    
    # Chercher le matériau dans la collection 'material' en utilisant son nom
    material = db.material.find_one({"name": material_name})
    
    # Si le matériau n'est pas trouvé, afficher un message d'erreur et retourner None
    if not material:
        print(f"Matiére non trouver: {material_name}")
        return None
    
    # Extraire le taux de réduction de CO2 du matériau
    co2_reduction_rate = material['co2_reduction_rate']
    # Calculer le CO2 économisé en multipliant le taux de réduction par la quantité
    co2_saved = co2_reduction_rate * quantity
    
    # Créer un dictionnaire représentant la transaction
    transaction = {
        "material": material_name,
        "quantity": quantity,
        "co2_saved": co2_saved,
        "date": datetime.datetime.utcnow()  # Utiliser l'heure UTC actuelle
    }
    
    # Insérer la transaction dans la collection 'transactions' de MongoDB
    result = db.transactions.insert_one(transaction)
    # Afficher l'ID de la transaction insérée
    print(f"Transaction inserted with ID: {result.inserted_id}")
    return transaction  # Retourner le dictionnaire de la transaction

# Fonction pour calculer le total de CO2 économisé
def get_total_co2_saved():
    # Accéder à la base de données MongoDB via les paramètres de configuration de Django
    db = settings.MONGO_DB
    
    # Récupérer toutes les transactions de la collection 'transactions'
    transactions = db.transactions.find()
    
    # Calculer le total de CO2 économisé en additionnant le 'co2_saved' de chaque transaction
    total_co2_saved = sum(t['co2_saved'] for t in transactions)# total de CO2 économisé en addition de toutes les transactions
    return total_co2_saved  # Retourner le total de CO2 économisé

# Fonction pour réinitialiser (supprimer) toutes les transactions
def reset_transactions():
    # Accéder à la base de données MongoDB via les paramètres de configuration de Django
    db = settings.MONGO_DB
    
    # Supprimer tous les documents de la collection 'transactions'
    result = db.transactions.delete_many({})
    # Afficher le nombre de transactions supprimées
    print(f"Deleted {result.deleted_count} transactions")

# Note: La fonction reset_transactions est définie deux fois, ce qui est redondant.
# Gardons une seule définition correcte :
def reset_transactions():
    db = settings.MONGO_DB
    result = db.transactions.delete_many({})
    print(f"Deleted {result.deleted_count} transactions")
