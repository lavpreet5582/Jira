from django.contrib import admin

from ticket.models import Ticket


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "reportee", "assignee", "title", "created_at")
    list_filter = ("reportee", "assignee", "created_at")
    search_fields = ("id", "title", "reportee__username", "assignee__username")
    raw_id_fields = ("reportee", "assignee")


admin.site.register(Ticket, TicketAdmin)
