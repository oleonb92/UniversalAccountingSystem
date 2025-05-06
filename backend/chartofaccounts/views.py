from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(household=self.request.user.household)

    def perform_create(self, serializer):
        serializer.save(household=self.request.user.household)