# Generated migration for comprehensive CMS models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0018_merge_20251215_1601'),
    ]

    operations = [
        # How We Operate Page with 10 Steps
        migrations.CreateModel(
            name='HowWeOperatePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hero_title', models.CharField(default='How We Operate', max_length=200)),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'How We Operate Page Content',
                'verbose_name_plural': 'How We Operate Page Content',
            },
        ),
        
        # Process Steps for How We Operate
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('step_number', models.CharField(max_length=10, default='01')),
                ('title', models.CharField(max_length=200, default='Step Title')),
                ('subtitle', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('bullet1', models.TextField(blank=True)),
                ('bullet2', models.TextField(blank=True)),
                ('bullet3', models.TextField(blank=True)),
                ('bullet4', models.TextField(blank=True)),
                ('bullet5', models.TextField(blank=True)),
                ('bullet6', models.TextField(blank=True)),
                ('bullet7', models.TextField(blank=True)),
                ('bullet8', models.TextField(blank=True)),
                ('bullet9', models.TextField(blank=True)),
                ('wordbreak', models.CharField(max_length=50, blank=True)),
                ('description1', models.TextField(blank=True)),
                ('description2', models.TextField(blank=True)),
                ('description3', models.TextField(blank=True)),
                ('description4', models.TextField(blank=True)),
                ('image_url', models.URLField(default='https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=600&fit=crop')),
                ('button_text', models.CharField(max_length=100, blank=True)),
                ('button_text2', models.CharField(max_length=100, blank=True)),
                ('button_text3', models.CharField(max_length=100, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Process Step',
                'verbose_name_plural': 'Process Steps',
            },
        ),
        
        # Services Page
        migrations.CreateModel(
            name='ServicesPageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hero_title', models.CharField(default='ORR Solutions - Listen. Solve. Optimise.', max_length=200)),
                ('hero_subtitle', models.TextField(default='We treat your organisation as a whole system — digital, regulatory, and living. We listen first, then design the right mix of advisory, systems, AI, and on-the-ground projects so you can move better and grow smarter too.')),
                ('pillars_title', models.CharField(default='The Three Pillars', max_length=200)),
                ('business_gp_title', models.CharField(default='ORR is your Business GP for', max_length=200)),
                ('business_gp_subtitle', models.CharField(default='complex systems — digital and living.', max_length=200)),
                ('business_gp_description', models.TextField(default='We listen to the whole organisation, solve with structure and insight, and optimise so you can grow with confidence.')),
                ('business_gp_button_text', models.CharField(default='Contact Us', max_length=50)),
                ('business_gp_image', models.CharField(default='/images/handshake.png', max_length=500)),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Services Page Content',
                'verbose_name_plural': 'Services Page Content',
            },
        ),
        
        # Service Stages for Services Page
        migrations.CreateModel(
            name='ServiceStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stage_number', models.PositiveIntegerField(default=1)),
                ('title', models.CharField(max_length=200, default='STAGE 1 - DISCOVER')),
                ('subtitle', models.CharField(max_length=200, default='Listen.')),
                ('description', models.TextField(default='Stage description')),
                ('focus_content', models.TextField(default='Focus points')),
                ('button_text', models.CharField(max_length=100, default='Learn More')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Service Stage',
                'verbose_name_plural': 'Service Stages',
            },
        ),
        
        # Service Pillars for Services Page
        migrations.CreateModel(
            name='ServicePillar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, default='Digital Systems, Automation & AI')),
                ('description', models.TextField(default='Pillar description')),
                ('button_text', models.CharField(max_length=50, default='Learn More')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Service Pillar',
                'verbose_name_plural': 'Service Pillars',
            },
        ),
        
        # Resources & Blogs Page
        migrations.CreateModel(
            name='ResourcesBlogsPageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hero_title', models.CharField(default='Resources & Client Portal', max_length=200)),
                ('hero_description1', models.TextField(default='Your digital HQ for business clarity, timelines, and real-time status. This isn\'t a traditional blog.')),
                ('hero_description2', models.TextField(default='Our resources are organized around the ORR client portal — a dashboard where you can read FAQs, download material, request meetings, and chat with a live operator or consultant.')),
                ('hero_description3', models.TextField(default='Instead of scattered articles, you get structured guidance that follows our live project — following blogs have insight, how-to — and real-time alerts. Everything is organized around live project management, AI marketing systems & implementation.')),
                ('hero_button1_text', models.CharField(default='Request access to the client portal', max_length=100)),
                ('hero_button2_text', models.CharField(default='Learn how we operate', max_length=100)),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Resources & Blogs Page Content',
                'verbose_name_plural': 'Resources & Blogs Page Content',
            },
        ),
        
        # Content Cards for Resources & Blogs Page
        migrations.CreateModel(
            name='ContentCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badge', models.CharField(max_length=50, default='Blog')),
                ('title', models.CharField(max_length=200, default='Content Title')),
                ('content', models.JSONField(default=list)),  # Array of content strings
                ('image_url', models.URLField(default='https://res.cloudinary.com/depeqzb6z/image/upload/v1765559589/21743692_6495306_uay57y.jpg')),
                ('button1_text', models.CharField(max_length=100, blank=True)),
                ('button2_text', models.CharField(max_length=100, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Content Card',
                'verbose_name_plural': 'Content Cards',
            },
        ),
        
        # Legal & Policy Page
        migrations.CreateModel(
            name='LegalPolicyPageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hero_title', models.CharField(default='Legacy & Policy', max_length=200)),
                ('hero_description', models.TextField(default='Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.')),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Legal & Policy Page Content',
                'verbose_name_plural': 'Legal & Policy Page Content',
            },
        ),
        
        # Policy Items for Legal & Policy Page
        migrations.CreateModel(
            name='PolicyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=10, default='01')),
                ('description', models.TextField(default='Policy description')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Policy Item',
                'verbose_name_plural': 'Policy Items',
            },
        ),
        
        # Contact Page
        migrations.CreateModel(
            name='ContactPageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hero_title', models.CharField(default='Contact Us', max_length=200)),
                ('contact_info_title', models.CharField(default='Contact Information', max_length=200)),
                ('contact_info_subtitle', models.CharField(default='Say something to start a live chat!', max_length=200)),
                ('phone_number', models.CharField(default='+012 3456 789', max_length=50)),
                ('email_address', models.EmailField(default='demo@gmail.com')),
                ('address', models.TextField(default='132 Dartmouth Street Boston, Massachusetts 02156 United States')),
                ('first_name_label', models.CharField(default='First Name', max_length=50)),
                ('last_name_label', models.CharField(default='Last Name', max_length=50)),
                ('email_label', models.CharField(default='Email', max_length=50)),
                ('phone_label', models.CharField(default='Phone Number', max_length=50)),
                ('subject_label', models.CharField(default='Select Subject?', max_length=50)),
                ('message_label', models.CharField(default='Message', max_length=50)),
                ('first_name_placeholder', models.CharField(default='John', max_length=50)),
                ('last_name_placeholder', models.CharField(default='Doe', max_length=50)),
                ('email_placeholder', models.CharField(default='your@email.com', max_length=50)),
                ('phone_placeholder', models.CharField(default='+1 012 3456 789', max_length=50)),
                ('message_placeholder', models.CharField(default='Write your message...', max_length=100)),
                ('subject_option_1', models.CharField(default='General Inquiry', max_length=100)),
                ('subject_option_2', models.CharField(default='General Inquiry', max_length=100)),
                ('subject_option_3', models.CharField(default='General Inquiry', max_length=100)),
                ('subject_option_4', models.CharField(default='General Inquiry', max_length=100)),
                ('submit_button_text', models.CharField(default='Send Message', max_length=50)),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Contact Page Content',
                'verbose_name_plural': 'Contact Page Content',
            },
        ),
    ]