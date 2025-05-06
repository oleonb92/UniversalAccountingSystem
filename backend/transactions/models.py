from django.db import models
from accounts.models import User
from households.models import Household
from chartofaccounts.models import Account  # ✅ Import corregido

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Ingreso'),
        ('EXPENSE', 'Gasto'),
        ('TRANSFER', 'Transferencia'),
    ]

    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    source_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='source_transactions'
    )
    destination_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='destination_transactions'
    )

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='transactions')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    is_imported = models.BooleanField(default=False)
    bank_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='confirmed')  # pending, confirmed, reconciled

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"