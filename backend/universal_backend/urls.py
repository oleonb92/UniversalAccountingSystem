from django.contrib import admin
from django.urls import path, include
from api.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # API grouped by app routers
    path("api/", include("api.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("households.urls")),     # households included once
    path("api/", include("transactions.urls")),
    path("api/", include("invitations.urls")),
    path("api/", include("audit.urls")),
    path("api/", include("chartofaccounts.urls")),

    # JWT tokens
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]