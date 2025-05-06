from django.db import models
from households.models import Household

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('ASSET', 'Activo'),
        ('LIABILITY', 'Pasivo'),
        ('EQUITY', 'Patrimonio'),
        ('INCOME', 'Ingreso'),
        ('EXPENSE', 'Gasto'),
        ('BANK', 'Cuenta Bancaria'),
        ('CREDIT', 'Tarjeta de Crédito'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='accounts')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"