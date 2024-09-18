# ticket/views.py
from django.core.mail import send_mail
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ticket.serializers import TicketSerializer
from ticket.models import Ticket
from rest_framework.decorators import action

class TicketViewset(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            tickets = Ticket.objects.filter(user=request.user)
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                ticket = serializer.save(user=request.user)  # Save the ticket with the authenticated user

                # Send email after ticket creation
                self.send_ticket_email(ticket, request.user.email, "created")

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(methods=["POST"], detail=True, url_path="update_ticket")
    def update_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                ticket = serializer.save()

                # Send email after ticket update
                self.send_ticket_email(ticket, request.user.email, "updated")

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            ticket = Ticket.objects.filter(pk=pk, user=request.user).first()
            if not ticket:
                return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
            ticket.delete()

            # Send email after ticket deletion
            self.send_ticket_email(ticket, request.user.email, "deleted")

            return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk, user=request.user)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Helper method to send email
    def send_ticket_email(self, ticket, email, action):
        subject = f"Your Ticket has been {action}"
        message = f"Dear {ticket.user},\n\nYour ticket with ID {ticket.id} has been {action}.\n\n" \
                  f"Title: {ticket.title}\nDescription: {ticket.body}\n\n" \
                  f"Thank you for using our service!"
        from_email = 'JiraClone@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
