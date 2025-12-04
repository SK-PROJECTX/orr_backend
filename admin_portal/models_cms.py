from django.db import models
from django.contrib.auth.models import User
from common.models import Audit


class HomePage(Audit):
    """Homepage content management"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Transform Your Business with ORR")
    hero_subtitle = models.TextField(default="Strategic Advisory, Digital Innovation, and Sustainable Growth Solutions")
    hero_cta_text = models.CharField(max_length=50, default="Get Started")
    hero_cta_link = models.URLField(default="/contact")
    hero_background_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    # About Section
    about_title = models.CharField(max_length=200, default="About ORR")
    about_content = models.TextField(default="We help organizations navigate complex challenges...")
    about_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Our Services")
    services_subtitle = models.TextField(blank=True)
    services_glow_image = models.CharField(max_length=500, blank=True, default="/images/services_glow.png")
    
    # Service Cards
    service_1_title = models.CharField(max_length=100, blank=True)
    service_1_description = models.TextField(blank=True)
    service_1_button = models.CharField(max_length=50, blank=True)
    service_2_title = models.CharField(max_length=100, blank=True)
    service_2_description = models.TextField(blank=True)
    service_2_button = models.CharField(max_length=50, blank=True)
    service_3_title = models.CharField(max_length=100, blank=True)
    service_3_description = models.TextField(blank=True)
    service_3_button = models.CharField(max_length=50, blank=True)
    
    # Contact Section
    contact_title = models.CharField(max_length=200, default="Get In Touch")
    contact_subtitle = models.TextField(blank=True)
    contact_email = models.EmailField(default="info@orr.com")
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"
    
    def __str__(self):
        return f"Homepage - {self.hero_title}"


class ServiceCard(Audit):
    """Service cards for homepage"""
    
    PILLAR_CHOICES = [
        ('strategic', 'Strategic Advisory & Compliance'),
        ('digital', 'Digital Systems, Automation & AI'),
        ('living', 'Living Systems & Regeneration'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="CSS icon class or emoji")
    pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class Testimonial(Audit):
    """Client testimonials"""
    
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100, blank=True)
    client_role = models.CharField(max_length=100, blank=True)
    testimonial_text = models.TextField()
    client_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class FAQ(Audit):
    """Frequently Asked Questions"""
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('services', 'Services'),
        ('pricing', 'Pricing'),
        ('process', 'Process'),
        ('support', 'Support'),
    ]
    
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question


class BlogPost(Audit):
    """Blog posts for homepage"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title


class ContactInfo(Audit):
    """Contact information"""
    
    company_name = models.CharField(max_length=100, default="ORR")
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Social Media
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Business Hours
    business_hours = models.TextField(blank=True, help_text="e.g., Mon-Fri: 9AM-5PM")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"{self.company_name} Contact Info"


class ApproachSection(Audit):
    """Approach section content"""
    
    title = models.CharField(max_length=200, default="Supporting Copy")
    paragraph_1 = models.TextField(default="Just like a skilled general practitioner, we start from your story not our framework. We take time to understand how your business really works before prescribing anything.")
    paragraph_2 = models.TextField(default="We're not a lone consultant — we're a central coordination layer with a distributed network behind it. When needed, we draw on specialists across continents, but you always deal with one point of contact: ORR, focused on what's best for you.")
    paragraph_3 = models.TextField(default="We fix what's slowing you down, strengthen systems around how your people actually work, and when deeper input is needed, we bring it in at the right moment — always in service of your goals.")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Approach Section"
        verbose_name_plural = "Approach Section"
    
    def __str__(self):
        return self.title


class BusinessSystemCard(Audit):
    """Business as living system cards"""
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='business_systems/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Business System Card"
        verbose_name_plural = "Business System Cards"
    
    def __str__(self):
        return self.title


class BusinessSystemSection(Audit):
    """Business as living system section"""
    
    title = models.CharField(max_length=200, default="Businesses as a Living System")
    subtitle = models.CharField(max_length=200, default="Think of your organisation like a body")
    card_1_title = models.CharField(max_length=100, default="Nervous System")
    card_1_description = models.TextField(default="Communication, data flow, and decision-making pathways")
    card_1_image = models.ImageField(upload_to='business_systems/', blank=True, null=True)
    card_2_title = models.CharField(max_length=100, default="Circulatory System")
    card_2_description = models.TextField(default="Cash flow, resource distribution, and value exchange")
    card_2_image = models.ImageField(upload_to='business_systems/', blank=True, null=True)
    card_3_title = models.CharField(max_length=100, default="Immune System")
    card_3_description = models.TextField(default="Risk management, compliance, and protective measures")
    card_3_image = models.ImageField(upload_to='business_systems/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Business System Section"
        verbose_name_plural = "Business System Section"
    
    def __str__(self):
        return self.title


class ORRRoleSection(Audit):
    """ORR Role section content"""
    
    title = models.CharField(max_length=200, default="ORR's Role")
    description = models.TextField(default="We act like specialist doctors for your business physiology - but we start from your symptoms and your priorities. We check the health of your system, diagnosis issues, and co-design solutions that your people can actually use, keeping everything working together over time.")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "ORR Role Section"
        verbose_name_plural = "ORR Role Section"
    
    def __str__(self):
        return self.title


class MessageStrip(Audit):
    """Message strip/testimonial section"""
    
    title = models.CharField(max_length=200, default="Message Strip")
    message = models.TextField(default="Businesses thrive like living organisms when all their systems work together *around real human needs*. ORR keeps your 'business physiology' in peak condition — aligning operations, communication, cash flow, compliance, data, and projects around the people you serve")
    user_image_1 = models.CharField(max_length=500, default="/images/user-1.jpg")
    user_image_2 = models.CharField(max_length=500, default="/images/user-2.jpg")
    user_image_3 = models.CharField(max_length=500, default="/images/user-3.jpg")
    user_image_4 = models.CharField(max_length=500, default="/images/user-4.jpg")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Message Strip"
        verbose_name_plural = "Message Strip"
    
    def __str__(self):
        return self.title


class ProcessStage(Audit):
    """Five stages process"""
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Process Stage"
        verbose_name_plural = "Process Stages"
    
    def __str__(self):
        return self.title


class ProcessSection(Audit):
    """Five stages section header"""
    
    title = models.CharField(max_length=200, default="How we work: Five Stages")
    subtitle = models.CharField(max_length=200, default="Every stage is built around you – your pace, your risk appetite, your resources")
    stage_1_title = models.CharField(max_length=100, default="Listen")
    stage_1_description = models.TextField(default="We start by understanding your current situation")
    stage_2_title = models.CharField(max_length=100, default="Diagnose")
    stage_2_description = models.TextField(default="Identify key issues and opportunities")
    stage_3_title = models.CharField(max_length=100, default="Design")
    stage_3_description = models.TextField(default="Co-create solutions that fit your context")
    stage_4_title = models.CharField(max_length=100, default="Implement")
    stage_4_description = models.TextField(default="Execute changes with your team")
    stage_5_title = models.CharField(max_length=100, default="Sustain")
    stage_5_description = models.TextField(default="Ensure lasting impact and continuous improvement")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Process Section"
        verbose_name_plural = "Process Section"
    
    def __str__(self):
        return self.title


class ORRReportSection(Audit):
    """ORR Report section content"""
    
    title = models.CharField(max_length=200, default="What you Get: The ORR Report")
    subtitle = models.TextField(default="After your first meeting, you receive a decision-ready ORR report designed to be immediately useful inside your organisation.")
    feature_1 = models.TextField(default="explain your situation in your language,")
    feature_1_image = models.CharField(max_length=500, default="/images/report_feature_1.png")
    feature_2 = models.TextField(default="highlights key issues and risks that affect your customers and teams")
    feature_2_image = models.CharField(max_length=500, default="/images/report_feature_2.png")
    feature_3 = models.TextField(default="proposes quick fixes and longer-term improvements that respect your constraints")
    feature_3_image = models.CharField(max_length=500, default="/images/report_feature_3.png")
    feature_4 = models.TextField(default="shows where advisory, digital systems/AI, or living-systems work will have most impact")
    feature_4_image = models.CharField(max_length=500, default="/images/report_feature_4.png")
    main_image = models.CharField(max_length=500, default="/images/orr_report_main.png")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "ORR Report Section"
        verbose_name_plural = "ORR Report Section"
    
    def __str__(self):
        return self.title


class SiteSettings(Audit):
    """Global site settings"""
    
    site_name = models.CharField(max_length=100, default="ORR")
    site_tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True)
    
    # Colors
    primary_color = models.CharField(max_length=7, default="#007bff")
    secondary_color = models.CharField(max_length=7, default="#6c757d")
    accent_color = models.CharField(max_length=7, default="#28a745")
    
    # Footer
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    # Legal
    privacy_policy_url = models.URLField(blank=True)
    terms_of_service_url = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"{self.site_name} Settings"