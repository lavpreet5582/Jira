from ticket.views import TicketViewset
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tickets", TicketViewset, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
]
