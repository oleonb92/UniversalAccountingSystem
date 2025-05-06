from rest_framework.routers import DefaultRouter
from .views import HouseholdViewSet

router = DefaultRouter()
router.register(r"households", HouseholdViewSet, basename="household")

urlpatterns = router.urls          #  ← solo esto, sin path() adicionales