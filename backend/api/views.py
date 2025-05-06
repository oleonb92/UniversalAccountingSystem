import logging
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import admin_required
from audit.models import AuditLog


User = get_user_model()
logger = logging.getLogger(__name__)

@api_view(['POST'])
def register_user(request):
    logger.info("🔐 Register attempt with data: %s", request.data)

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        logger.warning("❌ Missing username or password")
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        logger.warning("❌ Username already exists: %s", username)
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    logger.info("✅ User created: %s", username)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    logger.info("🔍 Profile requested by: %s", user)
    logger.debug("User.is_authenticated: %s", user.is_authenticated)
    logger.debug("User role: %s", getattr(user, "role", "undefined"))
    logger.debug("User household: %s", getattr(user.household, "name", None) if hasattr(user, "household") else "None")

    try:
        return Response({
            "username": user.username,
            "role": user.role,
            "household": user.household.name if user.household else None,
        })
    except Exception as e:
        logger.error("🔥 Error in profile_view: %s", str(e))
        return Response({"error": "Error fetching profile."}, status=500)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        logger.info("🔑 Token login attempt for: %s", attrs.get("username"))
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['household'] = self.user.household.name if self.user.household else None
        logger.info("✅ Token issued for user: %s", self.user.username)
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
    if getattr(request.user, "role", "") != "admin":
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all()
    user_data = []
    for user in users:
        if user.role == "admin":
            status_display = "admin"
        elif user.is_active:
            status_display = "approved"
        else:
            status_display = "pending" if not user.was_approved else "paused"

        user_data.append({
            "id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "date_joined": user.date_joined,
            "role": user.role,
            "household_name": getattr(user.household, "name", None) if hasattr(user, "household") else None,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "birthdate": user.birthdate,
            "was_approved": user.was_approved,
            "status": status_display,
            "show_pause": True if user.role == "member" and user.was_approved and user.is_active else False,
        })

    return Response(user_data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@admin_required
def approve_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.was_approved = True
        user.save()

        AuditLog.objects.create(
            action="approve",
            performed_by=request.user,
            target=user.username,
            details="User approved via admin panel"
        )

        return Response({"message": f"User '{user.username}' approved."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)   

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@admin_required
def deny_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()

        AuditLog.objects.create(
            action="reject",
            performed_by=request.user,
            target=user.username,
            details="User rejected via admin panel"
        )

        return Response({"message": f"User '{user.username}' denied."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@admin_required
def edit_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        print("🛠 PATCH user data:")
        print(" - username:", request.data.get("username"))
        print(" - first_name:", request.data.get("first_name"))
        print(" - last_name:", request.data.get("last_name"))
        print(" - email:", request.data.get("email"))
        print(" - role:", request.data.get("role"))
        print(" - birthdate:", request.data.get("birthdate"))
        user.username = request.data.get("username", user.username)
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.role = request.data.get("role", user.role)
        user.birthdate = request.data.get("birthdate", user.birthdate)
        user.save()

        AuditLog.objects.create(
            action="edit",
            performed_by=request.user,
            target=user.username,
            details="User profile edited by admin"
        )

        return Response({"message": "User updated."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@admin_required
def pause_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()

        AuditLog.objects.create(
            action="pause",
            performed_by=request.user,
            target=user.username,
            details=f"User {user.username} was paused by {request.user.username}"
        )

        return Response({"message": f"User '{user.username}' paused."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@admin_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()

        AuditLog.objects.create(
            action="delete",
            performed_by=request.user,
            target=user.username,
            details="User deleted from system"
        )

        return Response({"message": f"User '{user.username}' deleted successfully."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "birthdate": user.birthdate,
            "role": user.role,
            "household_name": user.household.name if user.household else None,
            "status": "approved" if user.is_active else ("paused" if user.was_approved else "pending"),
            "is_active": user.is_active,
            "was_approved": user.was_approved,
            "show_pause": user.was_approved and user.is_active and user.role == "member",
        }
        return Response(data)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)