from accounts.views import AuthViewset
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"accounts", AuthViewset, basename="accounts")

urlpatterns = [
    path("", include(router.urls)),
]
