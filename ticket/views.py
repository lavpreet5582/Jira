# ticket/views.py
import logging
from django.core.mail import send_mail
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ticket.serializers import TicketSerializer
from ticket.models import Ticket
from rest_framework.decorators import action


logger = logging.getLogger(__name__)


class TicketViewset(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            tickets = Ticket.objects.filter(reportee=request.user)
            serializer = TicketSerializer(tickets, many=True)
            logger.info("[GetTickets] %s No. of Tickets Found", len(tickets))
            return Response(serializer.data)
        except Exception as e:
            logger.exception(
                "[GetTickets] %s error found while fetching tickets", str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                ticket = serializer.save(
                    reportee=request.user
                )  # Save the ticket with the authenticated user
                logger.info(
                    "[CreateTicket] Ticket Created With ID %s and User %s",
                    ticket.id,
                    ticket.reportee.email,
                )

                # Send email after ticket creation
                self.send_ticket_email(ticket, request.user.email, "created")

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.exception(
                "[CreateTicket] Error While Creating Ticket: %s", str(serializer.errors)
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("[CreateTicket] Error While Creating Ticket: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=True, url_path="update_ticket")
    def update_ticket(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                ticket = serializer.save()
                logger.exception(
                    "[UpdateTicket] Ticket With ID %s Updated Successfully.", ticket.id
                )
                # Send email after ticket update
                self.send_ticket_email(ticket, request.user.email, "updated")

                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.exception(
                "[UpdateTicket] Error While Updating Ticket: %s", str(serializer.errors)
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            logger.exception("[UpdateTicket] Ticket Not Found With ID %s", pk)
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("[UpdateTicket] Error While Updating Ticket: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            ticket = Ticket.objects.filter(pk=pk, reportee=request.user).first()
            if not ticket:
                logger.exception(
                    "[DeleteTicket] Ticket Not Found With ID %s and User %s",
                    pk,
                    request.user.email,
                )
                return Response(
                    {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
                )
            ticket.delete()
            logger.info(
                "[DeleteTicket] Ticket With ID %s and User %s Deleted Successfully",
                pk,
                request.user.email,
            )
            # Send email after ticket deletion
            self.send_ticket_email(ticket, request.user.email, "deleted")

            return Response(
                {"message": "Ticket deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Ticket.DoesNotExist:
            logger.exception(
                "[DeleteTicket] Ticket Not Found With ID %s and User %s",
                pk,
                request.user.email,
            )
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("[DeleteTicket] Error While Deleting Ticket: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk, reportee=request.user)
            serializer = TicketSerializer(ticket)
            logger.info(
                "[GetTicketWithID] Ticket With ID %s and User %s Found Successfully",
                pk,
                request.user.email,
            )
            return Response(serializer.data)
        except Ticket.DoesNotExist:
            logger.exception(
                "[GetTicketWithID] Ticket Not Found With ID %s and User %s",
                pk,
                request.user.email,
            )
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(
                "[GetTicketWithID] Error While Deleting Ticket: %s", str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Helper method to send email
    def send_ticket_email(self, ticket, email, action):
        try:
            subject = f"Your Ticket has been {action}"
            message = (
                f"Dear {ticket.reportee},\n\nYour ticket with ID {ticket.id} has been {action}.\n\n"
                f"Title: {ticket.title}\nDescription: {ticket.body}\n\n"
                f"Thank you for using our service!"
            )
            from_email = "JiraClone@gmail.com"
            recipient_list = [email]
            logger.info("[SendMail] Sending Mail To User %s", email)
            send_mail(subject, message, from_email, recipient_list)
            logger.info("[SendMail] Mail Sent Successfully To User %s", email)
        except Exception as e:
            logger.exception("[SendMail] Error While Sending Mail: %s", str(e))
