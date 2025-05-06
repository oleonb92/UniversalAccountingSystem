from django.urls import path
from .views import (
    register_user,
    profile_view,
    list_users,
    approve_user,
    deny_user,
    edit_user,
    pause_user,
    delete_user,
    # list_audit_logs,
    get_user_detail
)

urlpatterns = [
    path('profile/', profile_view),
    # path("register/", register_user),  # <--- nueva ruta
    path("users/", list_users, name="list-users"),
    path("users/<int:user_id>/", get_user_detail, name="get-user-detail"),
    path("users/<int:user_id>/approve/", approve_user, name="approve-user"),
    path("users/<int:user_id>/deny/", deny_user, name="deny-user"),
    path("users/<int:user_id>/edit/", edit_user, name="edit-user"),
    path("users/<int:user_id>/pause/", pause_user, name="pause-user"),
    path("users/<int:user_id>/delete/", delete_user, name="delete-user"),
    # path("audit-logs/", list_audit_logs, name="list-audit-logs"),
]