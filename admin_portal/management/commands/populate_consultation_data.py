from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from admin_portal.models import Client, Meeting, Content, AdminRole, AdminProfile, SystemNotification
from payment.models import Invoice, Subscription
import random

class Command(BaseCommand):
    help = 'Populate database with sample consultation data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin users/consultants
        self.create_admin_users()
        
        # Create clients
        self.create_clients()
        
        # Create meetings
        self.create_meetings()
        
        # Create content/reports
        self.create_content()
        
        # Create billing data
        self.create_billing_data()
        
        # Create notifications
        self.create_notifications()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated consultation data!'))

    def create_admin_users(self):
        # Create admin role if it doesn't exist
        admin_role, created = AdminRole.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Admin with consultation permissions',
                'can_view_all_clients': True,
                'can_manage_meetings': True,
                'can_create_content': True,
                'can_publish_content': True,
            }
        )
        
        consultants = [
            {'username': 'john_consultant', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john@orr.com'},
            {'username': 'sarah_consultant', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah@orr.com'},
            {'username': 'mike_consultant', 'first_name': 'Mike', 'last_name': 'Davis', 'email': 'mike@orr.com'},
        ]
        
        for consultant_data in consultants:
            user, created = User.objects.get_or_create(
                username=consultant_data['username'],
                defaults={
                    'first_name': consultant_data['first_name'],
                    'last_name': consultant_data['last_name'],
                    'email': consultant_data['email'],
                    'is_staff': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                
                AdminProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': admin_role}
                )
                self.stdout.write(f'Created consultant: {user.get_full_name()}')

    def create_clients(self):
        clients_data = [
            {'username': 'alice_client', 'first_name': 'Alice', 'last_name': 'Brown', 'email': 'alice@company.com', 'company': 'Tech Corp'},
            {'username': 'bob_client', 'first_name': 'Bob', 'last_name': 'Wilson', 'email': 'bob@startup.com', 'company': 'StartupXYZ'},
            {'username': 'carol_client', 'first_name': 'Carol', 'last_name': 'Taylor', 'email': 'carol@enterprise.com', 'company': 'Enterprise Ltd'},
            {'username': 'david_client', 'first_name': 'David', 'last_name': 'Miller', 'email': 'david@business.com', 'company': 'Business Inc'},
            {'username': 'emma_client', 'first_name': 'Emma', 'last_name': 'Garcia', 'email': 'emma@solutions.com', 'company': 'Solutions Co'},
        ]
        
        for client_data in clients_data:
            user, created = User.objects.get_or_create(
                username=client_data['username'],
                defaults={
                    'first_name': client_data['first_name'],
                    'last_name': client_data['last_name'],
                    'email': client_data['email'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                
                Client.objects.get_or_create(
                    user=user,
                    defaults={
                        'company': client_data['company'],
                        'stage': random.choice(['discover', 'engage', 'implement', 'optimize']),
                        'primary_pillar': random.choice(['strategic', 'operational', 'financial', 'technological']),
                        'is_portal_active': True,
                    }
                )
                self.stdout.write(f'Created client: {user.get_full_name()} - {client_data["company"]}')

    def create_meetings(self):
        clients = Client.objects.all()
        consultants = User.objects.filter(is_staff=True)
        
        if not clients.exists() or not consultants.exists():
            self.stdout.write('No clients or consultants found. Skipping meetings.')
            return
        
        # Create scheduled meetings (future)
        for i in range(5):
            future_date = timezone.now() + timedelta(days=random.randint(1, 30))
            Meeting.objects.get_or_create(
                client=random.choice(clients),
                defaults={
                    'meeting_type': random.choice(['initial_consultation', 'follow_up', 'strategy_session', 'review']),
                    'requested_datetime': future_date,
                    'confirmed_datetime': future_date,
                    'duration_minutes': random.choice([30, 60, 90]),
                    'status': 'confirmed',
                    'agenda': f'Strategic consultation session {i+1} - Discuss business objectives and implementation roadmap',
                    'host': random.choice(consultants),
                }
            )
        
        # Create completed meetings (past)
        for i in range(8):
            past_date = timezone.now() - timedelta(days=random.randint(1, 90))
            Meeting.objects.get_or_create(
                client=random.choice(clients),
                defaults={
                    'meeting_type': random.choice(['initial_consultation', 'follow_up', 'strategy_session', 'review']),
                    'requested_datetime': past_date,
                    'confirmed_datetime': past_date,
                    'duration_minutes': random.choice([30, 60, 90]),
                    'status': 'completed',
                    'agenda': f'Completed consultation {i+1} - Business analysis and recommendations',
                    'meeting_notes': f'Meeting completed successfully. Discussed key strategic initiatives and next steps for implementation.',
                    'host': random.choice(consultants),
                }
            )
        
        self.stdout.write('Created sample meetings')

    def create_content(self):
        consultants = User.objects.filter(is_staff=True)
        
        if not consultants.exists():
            self.stdout.write('No consultants found. Skipping content.')
            return
        
        reports_data = [
            {'title': 'Q4 Strategic Analysis Report', 'status': 'published'},
            {'title': 'Digital Transformation Roadmap', 'status': 'published'},
            {'title': 'Operational Efficiency Assessment', 'status': 'draft'},
            {'title': 'Financial Performance Review', 'status': 'published'},
            {'title': 'Technology Infrastructure Audit', 'status': 'draft'},
            {'title': 'Market Expansion Strategy', 'status': 'published'},
            {'title': 'Risk Management Framework', 'status': 'draft'},
            {'title': 'Customer Experience Optimization', 'status': 'published'},
        ]
        
        for i, report_data in enumerate(reports_data):
            from django.utils.text import slugify
            slug = slugify(report_data['title'])
            if not slug:
                slug = f'report-{i+1}'
            
            Content.objects.get_or_create(
                title=report_data['title'],
                defaults={
                    'slug': slug,
                    'content_type': 'article',  # Use valid choice
                    'status': report_data['status'],
                    'stage': 'discover',  # Required field
                    'content': f'This is a comprehensive {report_data["title"].lower()} containing detailed analysis and recommendations.',
                    'author': random.choice(consultants),
                    'view_count': random.randint(5, 150),
                }
            )
        
        self.stdout.write('Created sample reports')

    def create_billing_data(self):
        clients = Client.objects.all()
        
        if not clients.exists():
            self.stdout.write('No clients found. Skipping billing data.')
            return
        
        # Create sample invoices
        for i in range(15):
            client = random.choice(clients)
            amount = random.choice([29.99, 49.99, 99.99, 199.99])
            status = random.choice(['Paid', 'Pending', 'Failed'])
            
            Invoice.objects.get_or_create(
                stripe_invoice_id=f'inv_{client.user.username}_{i}',
                defaults={
                    'user': client.user,
                    'billing_title': f'Consultation Services - {timezone.now().strftime("%b %Y")}',
                    'status': status,
                    'billing_date': timezone.now().date() - timedelta(days=random.randint(1, 180)),
                    'amount': amount,
                    'currency': 'USD',
                    'plan': random.choice(['Basic Plan', 'Pro Plan', 'Enterprise Plan']),
                    'users': 1,
                }
            )
        
        # Create sample subscriptions
        for client in clients[:3]:
            Subscription.objects.get_or_create(
                user=client.user,
                defaults={
                    'stripe_subscription_id': f'sub_{client.user.username}',
                    'stripe_customer_id': f'cus_{client.user.username}',
                    'plan_name': random.choice(['Basic Plan', 'Pro Plan', 'Enterprise Plan']),
                    'is_active': random.choice([True, False]),
                }
            )
        
        self.stdout.write('Created sample billing data')

    def create_notifications(self):
        admin_users = User.objects.filter(is_staff=True)
        clients = Client.objects.all()
        meetings = Meeting.objects.all()
        
        if not admin_users.exists():
            self.stdout.write('No admin users found. Skipping notifications.')
            return
        
        notifications_data = [
            {
                'notification_type': 'meeting_requested',
                'title': 'New Meeting Request',
                'message': 'New meeting requested by Bob Wilson',
                'related_client': clients.filter(user__first_name='Bob').first() if clients.filter(user__first_name='Bob').exists() else None,
                'related_meeting': meetings.filter(client__user__first_name='Bob').first() if meetings.filter(client__user__first_name='Bob').exists() else None,
            },
            {
                'notification_type': 'meeting_requested',
                'title': 'New Meeting Request',
                'message': 'New meeting requested by David Miller',
                'related_client': clients.filter(user__first_name='David').first() if clients.filter(user__first_name='David').exists() else None,
                'related_meeting': meetings.filter(client__user__first_name='David').first() if meetings.filter(client__user__first_name='David').exists() else None,
            },
            {
                'notification_type': 'meeting_requested',
                'title': 'New Meeting Request',
                'message': 'New meeting requested by Carol Taylor',
                'related_client': clients.filter(user__first_name='Carol').first() if clients.filter(user__first_name='Carol').exists() else None,
                'related_meeting': meetings.filter(client__user__first_name='Carol').first() if meetings.filter(client__user__first_name='Carol').exists() else None,
            },
            {
                'notification_type': 'system_error',
                'title': 'System Maintenance Completed',
                'message': 'Scheduled system maintenance has been completed successfully. All services are now fully operational.',
            },
            {
                'notification_type': 'ticket_created',
                'title': 'New Support Ticket',
                'message': 'A new support ticket has been created and requires attention.',
            },
        ]
        
        for i, notif_data in enumerate(notifications_data):
            for j, admin_user in enumerate(admin_users):
                SystemNotification.objects.get_or_create(
                    notification_type=notif_data['notification_type'],
                    title=notif_data['title'],
                    recipient=admin_user,
                    message=notif_data['message'],  # Include message in unique lookup
                    defaults={
                        'related_client': notif_data.get('related_client'),
                        'related_meeting': notif_data.get('related_meeting'),
                        'is_read': False,
                    }
                )
        
        self.stdout.write('Created sample notifications')