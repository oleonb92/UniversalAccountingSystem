from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(household=self.request.user.household)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, household=self.request.user.household)

    def get_object(self):
        obj = super().get_object()
        if obj.household != self.request.user.household:
            raise PermissionDenied("You do not have permission to access this transaction.")
        return obj

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.created_by != self.request.user:
            raise PermissionDenied("You can only edit your own transactions.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user:
            raise PermissionDenied("You can only delete your own transactions.")
        instance.delete()