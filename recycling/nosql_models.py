from djongo import models

class Material(models.Model):
    name = models.CharField(max_length=100)# Nom du matériau
    co2_reduction_rate = models.FloatField()  # kg de CO2 réduit par unité de matériau recyclé
    def __str__(self):
        return self.name

class Transaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()  # Quantité de matériau recyclé
    date = models.DateTimeField(auto_now_add=True)

    @property # Le décorateur @property transforme cette méthode en une propriété accessible comme un attribut
    def co2_saved(self):
        return self.material.co2_reduction_rate * self.quantity
