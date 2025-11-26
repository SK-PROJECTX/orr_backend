from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Ticket, Meeting, Content, SystemNotification, AuditLog, 
    AdminProfile, AdminRole
)


@receiver(post_save, sender=Ticket)
def ticket_created_notification(sender, instance, created, **kwargs):
    """Create notification when new ticket is created"""
    if created:
        # Notify assigned admin if any
        if instance.assigned_to:
            SystemNotification.objects.create(
                notification_type='ticket_created',
                title=f'New Ticket: {instance.ticket_id}',
                message=f'New ticket created: {instance.subject}',
                recipient=instance.assigned_to,
                related_ticket=instance,
                related_client=instance.client
            )
        
        # Create audit log
        AuditLog.objects.create(
            action='create',
            model_name='Ticket',
            object_id=str(instance.pk),
            description=f'Ticket created: {instance.ticket_id} - {instance.subject}'
        )


@receiver(post_save, sender=Meeting)
def meeting_created_notification(sender, instance, created, **kwargs):
    """Create notification when new meeting is requested"""
    if created:
        # Notify all admin users about new meeting request
        admin_users = User.objects.filter(
            admin_profile__role__can_manage_meetings=True,
            admin_profile__is_active=True
        )
        
        for admin_user in admin_users:
            SystemNotification.objects.create(
                notification_type='meeting_requested',
                title='New Meeting Request',
                message=f'New meeting requested by {instance.client.user.get_full_name()}',
                recipient=admin_user,
                related_meeting=instance,
                related_client=instance.client
            )


@receiver(post_save, sender=Content)
def content_published_notification(sender, instance, created, **kwargs):
    """Create audit log when content is published"""
    if not created and instance.status == 'published' and instance.published_at:
        AuditLog.objects.create(
            action='publish',
            model_name='Content',
            object_id=str(instance.pk),
            description=f'Content published: {instance.title}'
        )


@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    """Create admin profile for staff users"""
    if created and instance.is_staff:
        # Get or create default admin role
        admin_role, _ = AdminRole.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Default admin role',
                'can_view_all_clients': True,
                'can_manage_tickets': True,
                'can_manage_meetings': True,
                'can_create_content': True,
                'can_view_analytics': True,
            }
        )
        
        AdminProfile.objects.get_or_create(
            user=instance,
            defaults={
                'role': admin_role,
                'is_active': True
            }
        )


@receiver(post_delete, sender=Content)
def content_deleted_audit(sender, instance, **kwargs):
    """Create audit log when content is deleted"""
    AuditLog.objects.create(
        action='delete',
        model_name='Content',
        object_id=str(instance.pk),
        description=f'Content deleted: {instance.title}'
    )