from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ticket.serializers import TicketSerializer
from ticket.models import Ticket


class TicketViewset(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            tickets = Ticket.objects.all()  # Fetch all tickets
            serializer = TicketSerializer(tickets, many=True)  # Serialize the data
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )  # Return serialized data
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
