from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import PendingInvitation
from households.models import Household
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_pending_invitations(request):
    user = request.user
    if user.role != 'admin':
        return Response({"detail": "Only admins can view pending invitations."}, status=403)

    invitations = PendingInvitation.objects.filter(household=user.household, is_approved=False)
    data = [{"username": inv.username, "requested_at": inv.requested_at} for inv in invitations]
    return Response(data)

# class UserUpdateView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'