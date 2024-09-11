from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from ticket.serializers import TicketSerializer

from ticket.models import Ticket


# Create your views here.
class TicketViewset(ViewSet):
    def list(self, request):
        ticktets = Ticket.objects.all()
        serializer = TicketSerializer(ticktets, many=True)
        return Response(serializer.data)
