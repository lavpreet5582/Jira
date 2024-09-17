from ticket.models import Ticket
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    class Meta:
        model = Ticket
        fields = ["id", "user_email", "title", "body", "created_at"]