from ticket.models import Ticket
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    reportee_email = serializers.ReadOnlyField(source="reportee.email")
    reportee_name = serializers.SerializerMethodField()
    assignee_email = serializers.ReadOnlyField(source="assignee.email")
    assignee_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "reportee_email",
            "reportee_name",
            "assignee_email",
            "assignee_name",
            "title",
            "body",
            "created_at",
            "modified_at",
        ]

    def get_reportee_name(self, obj):
        return obj.reportee.get_full_name()

    def get_assignee_name(self, obj):
        if obj.assignee:
            return obj.assignee.get_full_name()
        return None
    
