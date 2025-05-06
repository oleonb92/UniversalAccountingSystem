from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'amount',
            'date',
            'description',
            'category',
            'source_account',
            'destination_account',
            'is_imported',
            'bank_transaction_id',
            'status',
            'created_at',
            'modified_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'modified_at']