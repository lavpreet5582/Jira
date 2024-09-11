from django.contrib import admin

from ticket.models import Ticket

# Register your models here.
class TicketAdmin(admin.ModelAdmin):    
    list_display = ('id', 'user', 'title', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('id', 'title','user__username')

admin.site.register(Ticket, TicketAdmin)