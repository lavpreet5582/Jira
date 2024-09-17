from ticket.models import Ticket
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")
    user_name = serializers.ReadOnlyField(source="user.first_name")
    class Meta:
        model = Ticket
        fields = ["id", "user_email", "user_name", "title", "body", "created_at"]