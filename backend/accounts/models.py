from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    household = models.ForeignKey(
        'households.Household',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='members'
    )

    was_approved = models.BooleanField(default=False)
    birthdate = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
class PendingInvitation(models.Model):
    username = models.CharField(max_length=150)
    household = models.ForeignKey('households.Household', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} requested to join {self.household.name}"