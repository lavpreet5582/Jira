from django.db import models
from accounts.models import User

# Create your models here.


class PriorityChoices:
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


class StatusChoices:
    BACKLOG = 0
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        (PriorityChoices.MEDIUM, "Medium"),
        (PriorityChoices.HIGH, "High"),
        (PriorityChoices.CRITICAL, "Critical"),
    ]
    STATUS_CHOICES = [
        (StatusChoices.BACKLOG, "Backlog"),
        (StatusChoices.PENDING, "Pending"),
        (StatusChoices.IN_PROGRESS, "In Progress"),
        (StatusChoices.COMPLETED, "Completed"),
    ]
    reportee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tickets"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=StatusChoices.PENDING,
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=PriorityChoices.MEDIUM,
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
