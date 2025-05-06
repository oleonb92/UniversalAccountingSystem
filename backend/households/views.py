from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Household
from .serializers import HouseholdSerializer

class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all().order_by("name")
    serializer_class = HouseholdSerializer
    permission_classes = [permissions.IsAuthenticated]  # ajusta si quieres que sea público