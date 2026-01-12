from django.db import models
from django.contrib.auth.models import User
from common.models import Audit
from django.utils.text import slugify

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


class ServicesPage(Audit):
    """Services page content management"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="ORR Solutions - Listen. Solve. Optimise.")
    hero_subtitle = models.TextField(default="We treat your organisation as a whole system — digital, regulatory, and living. We listen first, then design the right mix of advisory, systems, AI, and on-the-ground projects so you can move better and grow smarter too.")
    
    # Process Stages
    stage_1_title = models.CharField(max_length=100, default="STAGE 1 - DISCOVER")
    stage_1_subtitle = models.CharField(max_length=100, default="Listen.")
    stage_1_description = models.TextField(default="We start simple: one calm conversation and a quick scan of your reality.")
    stage_1_focus = models.TextField(default="We focus on:\n• Your context, people, and pressures\n• Regulatory, operational, data, and environmental risks\n• Which questions actually matter")
    stage_1_button_text = models.CharField(max_length=50, default="Sign up")
    
    stage_2_title = models.CharField(max_length=100, default="STAGE 2 - DIAGNOSE")
    stage_2_subtitle = models.CharField(max_length=100, default="Think. Then listen again.")
    stage_2_description = models.TextField(default="We turn symptoms into a clear map of problems and opportunities across three pillars.")
    stage_2_focus = models.TextField(default="What happens here:\n• Bottleneck and process mapping\n• Compliance, governance, and risk review\n• Data and living systems scan\n• Prioritised list: urgent, high leverage, later")
    stage_2_button_text = models.CharField(max_length=50, default="Learn More")
    
    stage_3_title = models.CharField(max_length=100, default="STAGE 3 - DESIGN")
    stage_3_subtitle = models.CharField(max_length=100, default="Design.")
    stage_3_description = models.TextField(default="We design practical structures not theory decks.")
    stage_3_focus = models.TextField(default="Typical Outputs:\n• SOPs and standardised workflows\n• Communication and decision pathways\n• Tech stacks, integration and AI use-case\n• Simple concepts for field or nurture projects\n• Clean, structured data ready for reporting")
    stage_3_button_1_text = models.CharField(max_length=50, default="Sign up")
    stage_3_button_2_text = models.CharField(max_length=100, default="Learn More on living systems & augmentation")
    
    stage_4_title = models.CharField(max_length=100, default="STAGE 4 - DEPLOY")
    stage_4_subtitle = models.CharField(max_length=100, default="Solve in practice.")
    stage_4_description = models.TextField(default="Design becomes reality with guided implementation.")
    stage_4_focus = models.TextField(default="Deployment can include:\n• Admin and records setup\n• Client logging, pipeline, and follow-up flows\n• KPI fit dashboards with AI summaries\n• Staff training in the tools you already use\n• Connecting with external providers where needed")
    stage_4_button_text = models.CharField(max_length=50, default="Contact Us")
    
    stage_5_title = models.CharField(max_length=100, default="STAGE 5 - GROW")
    stage_5_subtitle = models.CharField(max_length=100, default="Optimise.")
    stage_5_description = models.TextField(default="Once systems are live, we keep them learning.")
    stage_5_focus = models.TextField(default="How we support growth:\n• Ongoing data capture and light analytics\n• Quarterly reviews and system tuning\n• AI-assisted monitoring and early warnings\n• Scenario and 'what if' thinking\n• Light, regular check-ins — your systems clinic")
    stage_5_button_text = models.CharField(max_length=50, default="Sign up")
    
    # Three Pillars Section
    pillars_title = models.CharField(max_length=200, default="The Three Pillars")
    
    pillar_1_title = models.CharField(max_length=100, default="Digital Systems, Automation & AI")
    pillar_1_description = models.TextField(default="SOPs, workflows, portals, dashboards, and AI helpers that make work flow with less effort and fewer surprises.")
    pillar_1_button_text = models.CharField(max_length=50, default="Learn More")
    
    pillar_2_title = models.CharField(max_length=100, default="Strategic Advisory & Compliance")
    pillar_2_description = models.TextField(default="Short, sharp clarity on rules, risk, and direction — from regulation and ESG to biotech and environmental questions.")
    pillar_2_button_text = models.CharField(max_length=50, default="Learn More")
    
    pillar_3_title = models.CharField(max_length=100, default="Living Systems & Regeneration")
    pillar_3_description = models.TextField(default="Support for land, water, species, and ecosystems — from production systems to restoration and incident response.")
    pillar_3_button_text = models.CharField(max_length=50, default="Learn More")
    
    # Business GP Section
    business_gp_title = models.CharField(max_length=200, default="ORR is your Business GP for")
    business_gp_subtitle = models.CharField(max_length=200, default="complex systems — digital and living.")
    business_gp_description = models.TextField(default="We listen to the whole organisation, solve with structure and insight, and optimise so you can grow with confidence.")
    business_gp_button_text = models.CharField(max_length=50, default="Contact Us")
    business_gp_image = models.CharField(max_length=500, default="/images/handshake.png")
    
    # Services Overview Section
    services_overview_title = models.CharField(max_length=200, default="SERVICES OVERVIEW")
    
    service_1_title = models.CharField(max_length=100, default="Strategic Advisory & Compliance")
    service_1_description = models.TextField(default="We deliver clarity to complexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving landscapes with confidence. Our approach combines deep technical insight with strategic foresight, ensuring every initiative is compliant, sustainable, and built for growth.")
    service_1_image = models.CharField(max_length=500, default="/man picture.jpg")
    service_1_button_text = models.CharField(max_length=50, default="Learn More")
    
    service_2_title = models.CharField(max_length=100, default="Operational Systems & Infrastructure")
    service_2_description = models.TextField(default="We design, build and streamline the systems that power modern organizations. Whether it's creating SOPs, structuring onboarding workflows, or coordinating complex office setups, we turn operations into well- functioning ecosystems. Our trusted network of builders, finishers, and tech specialists delivers reliability from planning to execution.")
    service_2_image = models.CharField(max_length=500, default="/man picture.jpg")
    service_2_button_text = models.CharField(max_length=50, default="Learn More")
    
    # Data Intelligence Section
    data_intelligence_title = models.CharField(max_length=200, default="Data Intelligence & Concierge Solutions")
    data_intelligence_description = models.TextField(default="Insight meets adaptability. We help organizations turn data into decisions through advanced analytics, KPI dashboards, and predictive modeling. Alongside our concierge division, we offer personalized support and problem-solving — delivering smart, human solutions for both business and lifestyle needs with precision and discretion.")
    data_intelligence_image = models.CharField(max_length=500, default="/man picture.jpg")
    data_intelligence_button_text = models.CharField(max_length=50, default="Learn More")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Services Page Content"
        verbose_name_plural = "Services Page Content"
    
    def __str__(self):
        return f"Services Page - {self.hero_title}"


class ResourcesBlogsPage(Audit):
    """Resources & Blogs page content management"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Resources / Blogs")
    hero_subtitle = models.TextField(default="Lorem ipsm ticles, practical guides, and future-focused insights on digital transformation, AI, software development, and cloud innovation, written to help your business scale with confidence.")
    
    # Blog Cards (4 cards)
    blog_card_1_title = models.CharField(max_length=200, default="Mobile Apps & PWAs for Maltese Insurers: Boost Engagement | Born Digital")
    blog_card_1_category = models.CharField(max_length=50, default="Article")
    blog_card_1_image = models.CharField(max_length=500, default="/images/image.png")
    
    blog_card_2_title = models.CharField(max_length=200, default="Mobile Apps & PWAs for Maltese Insurers: Boost Engagement | Born Digital")
    blog_card_2_category = models.CharField(max_length=50, default="Article")
    blog_card_2_image = models.CharField(max_length=500, default="/images/image.png")
    
    blog_card_3_title = models.CharField(max_length=200, default="Mobile Apps & PWAs for Maltese Insurers: Boost Engagement | Born Digital")
    blog_card_3_category = models.CharField(max_length=50, default="Article")
    blog_card_3_image = models.CharField(max_length=500, default="/images/image.png")
    
    blog_card_4_title = models.CharField(max_length=200, default="Mobile Apps & PWAs for Maltese Insurers: Boost Engagement | Born Digital")
    blog_card_4_category = models.CharField(max_length=50, default="Article")
    blog_card_4_image = models.CharField(max_length=500, default="/images/image.png")
    
    # Admin Tips Section
    admin_tips_title = models.CharField(max_length=200, default="Admin Tips")
    
    tip_1_number = models.CharField(max_length=10, default="01")
    tip_1_title = models.CharField(max_length=100, default="Lorem ipsum")
    tip_1_description = models.TextField(default="Lorem ipsum jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    
    tip_2_number = models.CharField(max_length=10, default="02")
    tip_2_title = models.CharField(max_length=100, default="Lorem ipsum")
    tip_2_description = models.TextField(default="Lorem ipsum jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our experts help clients navigate complex requirements with confidence.")
    
    tip_3_number = models.CharField(max_length=10, default="03")
    tip_3_title = models.CharField(max_length=100, default="Lorem ipsum")
    tip_3_description = models.TextField(default="Lorem ipsum jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards.")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Resources & Blogs Page Content"
        verbose_name_plural = "Resources & Blogs Page Content"
    
    def __str__(self):
        return f"Resources & Blogs Page - {self.hero_title}"


class LegacyPolicyPage(Audit):
    """Legacy & Policy page content management"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Legacy & Policy")
    hero_description = models.TextField(default="Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    
    # Policy Items
    policy_item_1_number = models.CharField(max_length=10, default="01")
    policy_item_1_description = models.TextField(default="Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    
    policy_item_2_number = models.CharField(max_length=10, default="02")
    policy_item_2_description = models.TextField(default="Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    
    policy_item_3_number = models.CharField(max_length=10, default="03")
    policy_item_3_description = models.TextField(default="Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Legacy & Policy Page Content"
        verbose_name_plural = "Legacy & Policy Page Content"
    
    def __str__(self):
        return f"Legacy & Policy Page - {self.hero_title}"


class ContactPage(Audit):
    """Contact page content management"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Contact Us")
    
    # Contact Information
    contact_info_title = models.CharField(max_length=200, default="Contact Information")
    contact_info_subtitle = models.CharField(max_length=200, default="Say something to start a live chat!")
    
    phone_number = models.CharField(max_length=50, default="+012 3456 789")
    email_address = models.EmailField(default="demo@gmail.com")
    address = models.TextField(default="132 Dartmouth Street Boston, Massachusetts 02156 United States")
    
    # Form Labels
    first_name_label = models.CharField(max_length=50, default="First Name")
    last_name_label = models.CharField(max_length=50, default="Last Name")
    email_label = models.CharField(max_length=50, default="Email")
    phone_label = models.CharField(max_length=50, default="Phone Number")
    subject_label = models.CharField(max_length=50, default="Select Subject?")
    message_label = models.CharField(max_length=50, default="Message")
    
    # Form Placeholders
    first_name_placeholder = models.CharField(max_length=50, default="John")
    last_name_placeholder = models.CharField(max_length=50, default="Doe")
    email_placeholder = models.CharField(max_length=50, default="your@email.com")
    phone_placeholder = models.CharField(max_length=50, default="+1 012 3456 789")
    message_placeholder = models.CharField(max_length=100, default="Write your message...")
    
    # Subject Options
    subject_option_1 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_2 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_3 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_4 = models.CharField(max_length=100, default="General Inquiry")
    
    # Submit Button
    submit_button_text = models.CharField(max_length=50, default="Send Message")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"
    
    def __str__(self):
        return f"Contact Page - {self.hero_title}"


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


# NEW COMPREHENSIVE CMS MODELS

class HowWeOperatePageContent(Audit):
    """How We Operate page content management"""
    
    hero_title = models.CharField(max_length=200, default="How We Operate")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "How We Operate Page Content"
        verbose_name_plural = "How We Operate Page Content"
    
    def __str__(self):
        return f"How We Operate - {self.hero_title}"


class ProcessStep(Audit):
    """Process steps for How We Operate page"""
    
    step_number = models.CharField(max_length=10, default="01")
    title = models.CharField(max_length=200, default="Step Title")
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    bullet1 = models.TextField(blank=True)
    bullet2 = models.TextField(blank=True)
    bullet3 = models.TextField(blank=True)
    bullet4 = models.TextField(blank=True)
    bullet5 = models.TextField(blank=True)
    bullet6 = models.TextField(blank=True)
    bullet7 = models.TextField(blank=True)
    bullet8 = models.TextField(blank=True)
    bullet9 = models.TextField(blank=True)
    wordbreak = models.CharField(max_length=50, blank=True)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    description3 = models.TextField(blank=True)
    description4 = models.TextField(blank=True)
    image_url = models.URLField(default="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=600&fit=crop")
    button_text = models.CharField(max_length=100, blank=True)
    button_text2 = models.CharField(max_length=100, blank=True)
    button_text3 = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Process Step"
        verbose_name_plural = "Process Steps"
    
    def __str__(self):
        return f"{self.step_number} - {self.title}"


class ServicesPageContent(Audit):
    """Services page content management"""
    
    hero_title = models.CharField(max_length=200, default="ORR Solutions - Listen. Solve. Optimise.")
    hero_subtitle = models.TextField(default="We treat your organisation as a whole system — digital, regulatory, and living. We listen first, then design the right mix of advisory, systems, AI, and on-the-ground projects so you can move better and grow smarter too.")
    pillars_title = models.CharField(max_length=200, default="The Three Pillars")
    business_gp_title = models.CharField(max_length=200, default="ORR is your Business GP for")
    business_gp_subtitle = models.CharField(max_length=200, default="complex systems — digital and living.")
    business_gp_description = models.TextField(default="We listen to the whole organisation, solve with structure and insight, and optimise so you can grow with confidence.")
    business_gp_button_text = models.CharField(max_length=50, default="Contact Us")
    business_gp_image = models.CharField(max_length=500, default="/images/handshake.png")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Services Page Content"
        verbose_name_plural = "Services Page Content"
    
    def __str__(self):
        return f"Services Page - {self.hero_title}"


class ServiceStage(Audit):
    """Service stages for Services page"""
    
    stage_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200, default="STAGE 1 - DISCOVER")
    subtitle = models.CharField(max_length=200, default="Listen.")
    description = models.TextField(default="Stage description")
    focus_content = models.TextField(default="Focus points")
    button_text = models.CharField(max_length=100, default="Learn More")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Service Stage"
        verbose_name_plural = "Service Stages"
    
    def __str__(self):
        return f"Stage {self.stage_number} - {self.title}"


class ServicePillar(Audit):
    """Service pillars for Services page"""
    
    title = models.CharField(max_length=200, default="Digital Systems, Automation & AI")
    description = models.TextField(default="Pillar description")
    button_text = models.CharField(max_length=50, default="Learn More")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Service Pillar"
        verbose_name_plural = "Service Pillars"
    
    def __str__(self):
        return self.title


class ResourcesBlogsPageContent(Audit):
    """Resources & Blogs page content management"""
    
    hero_title = models.CharField(max_length=200, default="Resources & Client Portal")
    hero_description1 = models.TextField(default="Your digital HQ for business clarity, timelines, and real-time status. This isn't a traditional blog.")
    hero_description2 = models.TextField(default="Our resources are organized around the ORR client portal — a dashboard where you can read FAQs, download material, request meetings, and chat with a live operator or consultant.")
    hero_description3 = models.TextField(default="Instead of scattered articles, you get structured guidance that follows our live project — following blogs have insight, how-to — and real-time alerts. Everything is organized around live project management, AI marketing systems & implementation.")
    hero_button1_text = models.CharField(max_length=100, default="Request access to the client portal")
    hero_button2_text = models.CharField(max_length=100, default="Learn how we operate")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Resources & Blogs Page Content"
        verbose_name_plural = "Resources & Blogs Page Content"
    
    def __str__(self):
        return f"Resources & Blogs Page - {self.hero_title}"


class ContentCard(Audit):
    """Content cards for Resources & Blogs page"""
    card_slug = models.SlugField(max_length=255, unique=True, blank=True, null=True) 
    badge = models.CharField(max_length=50, default="Blog")
    title = models.CharField(max_length=200, default="Content Title")
    content = models.JSONField(default=list)  # Array of content strings
    image_url = models.URLField(default="https://res.cloudinary.com/depeqzb6z/image/upload/v1765559589/21743692_6495306_uay57y.jpg")
    button1_text = models.CharField(max_length=100, blank=True)
    button2_text = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["order"]
    
    def __str__(self):
        return self.title


class LegalPolicyPageContent(Audit):
    """Legal & Policy page content management"""
    
    hero_title = models.CharField(max_length=200, default="Legacy & Policy")
    hero_description = models.TextField(default="Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Legal & Policy Page Content"
        verbose_name_plural = "Legal & Policy Page Content"
    
    def __str__(self):
        return f"Legal & Policy Page - {self.hero_title}"


class PolicyItem(Audit):
    """Policy items for Legal & Policy page"""
    
    number = models.CharField(max_length=10, default="01")
    description = models.TextField(default="Policy description")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Policy Item"
        verbose_name_plural = "Policy Items"
    
    def __str__(self):
        return f"{self.number} - Policy Item"


class ContactPageContent(Audit):
    """Contact page content management"""
    
    hero_title = models.CharField(max_length=200, default="Contact Us")
    contact_info_title = models.CharField(max_length=200, default="Contact Information")
    contact_info_subtitle = models.CharField(max_length=200, default="Say something to start a live chat!")
    phone_number = models.CharField(max_length=50, default="+012 3456 789")
    email_address = models.EmailField(default="demo@gmail.com")
    address = models.TextField(default="132 Dartmouth Street Boston, Massachusetts 02156 United States")
    first_name_label = models.CharField(max_length=50, default="First Name")
    last_name_label = models.CharField(max_length=50, default="Last Name")
    email_label = models.CharField(max_length=50, default="Email")
    phone_label = models.CharField(max_length=50, default="Phone Number")
    subject_label = models.CharField(max_length=50, default="Select Subject?")
    message_label = models.CharField(max_length=50, default="Message")
    first_name_placeholder = models.CharField(max_length=50, default="John")
    last_name_placeholder = models.CharField(max_length=50, default="Doe")
    email_placeholder = models.CharField(max_length=50, default="your@email.com")
    phone_placeholder = models.CharField(max_length=50, default="+1 012 3456 789")
    message_placeholder = models.CharField(max_length=100, default="Write your message...")
    subject_option_1 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_2 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_3 = models.CharField(max_length=100, default="General Inquiry")
    subject_option_4 = models.CharField(max_length=100, default="General Inquiry")
    submit_button_text = models.CharField(max_length=50, default="Send Message")
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"
    
    def __str__(self):
        return f"Contact Page - {self.hero_title}"


# NEW SERVICE PILLAR PAGES

class StrategicAdvisoryPageContent(Audit):
    """Strategic Advisory & Compliance page content management"""
    
    hero_title = models.CharField(max_length=200, default="Strategic Advisory & Compliance")
    hero_subtitle = models.TextField(default="We deliver clarity to complexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving landscapes with confidence.")
    hero_description = models.TextField(default="Our approach combines deep technical insight with strategic foresight, ensuring every initiative is compliant, sustainable, and built for growth.")
    hero_image = models.URLField(default="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop")
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Our Strategic Services")
    service_1_title = models.CharField(max_length=100, default="Regulatory Compliance")
    service_1_description = models.TextField(default="Navigate complex regulatory frameworks with confidence")
    service_2_title = models.CharField(max_length=100, default="ESG & Sustainability")
    service_2_description = models.TextField(default="Build sustainable business practices that drive growth")
    service_3_title = models.CharField(max_length=100, default="Risk Management")
    service_3_description = models.TextField(default="Identify and mitigate business risks proactively")
    
    # Process Section
    process_title = models.CharField(max_length=200, default="Our Strategic Process")
    process_subtitle = models.CharField(max_length=200, default="Listen . Solve . Optimize")
    process_description = models.TextField(default="Like your Business GP, we diagnose compliance challenges and prescribe strategic solutions tailored to your organization's unique context.")
    process_step_1_title = models.CharField(max_length=100, default="Listen & Report")
    process_step_1_subtitle = models.CharField(max_length=100, default="(Initial Discovery)")
    process_step_1 = models.TextField(default="We start with a focused initial meeting to understand your compliance challenges, regulatory environment, and strategic objectives.")
    process_step_2_title = models.CharField(max_length=100, default="Decide: Document or Partnership")
    process_step_2 = models.TextField(default="Once you receive the report, you choose your path forward: Use the report independently or engage ORR for ongoing implementation support.")
    process_step_3_title = models.CharField(max_length=100, default="Optimize (For Clients Who Continue)")
    process_step_3 = models.TextField(default="For clients who choose ongoing partnership, we move into implementation and optimization.")
    process_step_4 = models.TextField(default="With systems live, we provide continuous monitoring, regular reviews, and proactive adjustments to ensure your compliance strategies evolve with changing regulations and business needs.")
    process_step_4_title = models.CharField(max_length=100, default="Grow")
    # Network Section
    network_title = models.CharField(max_length=200, default="The ORR Network Advantage")
    network_description = models.TextField(default="Complex compliance challenges require diverse expertise. We activate our global network of specialists to deliver comprehensive solutions.")
    network_cards = models.JSONField(default=list)
    
    # Digital Solutions Section
    digital_title = models.CharField(max_length=200, default="Digital Solutions for")
    digital_subtitle = models.CharField(max_length=200, default="Compliance Management")
    digital_description = models.TextField(default="We don't just advise — we build digital infrastructure to operationalize compliance:")
    digital_image_alt = models.CharField(max_length=200, default="Network visualization showing connected nodes and data flows")
    digital_who_is_this_for = models.JSONField(default=list)
    digital_features = models.JSONField(default=list)
    
    # Case Example Section
    case_challenge = models.TextField(blank=True)
    case_solution = models.TextField(blank=True)
    case_result = models.TextField(blank=True)
    case_image_alt = models.CharField(max_length=200, default="Business documents and reports on a desk")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Transform Your Strategy?")
    cta_description = models.TextField(default="Let's discuss how our strategic advisory services can help your organization thrive.")
    cta_button_text = models.CharField(max_length=50, default="Get Started")
    
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Strategic Advisory Page Content"
        verbose_name_plural = "Strategic Advisory Page Content"
    
    def __str__(self):
        return f"Strategic Advisory - {self.hero_title}"


class OperationalSystemsPageContent(Audit):
    """Operational Systems & Infrastructure page content management"""
    
    hero_title = models.CharField(max_length=200, default="Operational Systems & Infrastructure")
    hero_subtitle = models.TextField(default="We design, build and streamline the systems that power modern organizations. Whether it's creating SOPs, structuring workflows, or coordinating complex setups.")
    hero_description = models.TextField(default="We turn operations into well-functioning ecosystems. Our trusted network of builders and tech specialists delivers reliability from planning to execution.")
    hero_image = models.URLField(default="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop")
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Our Operational Services")
    service_1_title = models.CharField(max_length=100, default="Process Optimization")
    service_1_description = models.TextField(default="Streamline workflows and eliminate operational bottlenecks")
    service_2_title = models.CharField(max_length=100, default="System Integration")
    service_2_description = models.TextField(default="Connect your tools and platforms for seamless operations")
    service_3_title = models.CharField(max_length=100, default="Infrastructure Setup")
    service_3_description = models.TextField(default="Build robust operational foundations that scale")
    
    # Process Section
    process_title = models.CharField(max_length=200, default="Our Implementation Process")
    process_description = models.TextField(default="Just like your Business GP, we follow a systematic diagnostic and treatment approach to restore operational health.")
    process_step_1 = models.TextField(default="Current State Analysis")
    process_step_2 = models.TextField(default="System Design")
    process_step_3 = models.TextField(default="Implementation & Testing")
    process_step_4 = models.TextField(default="Training & Optimization")
    
    # Case Example Section
    case_challenge = models.TextField(blank=True)
    case_solution = models.TextField(blank=True)
    case_result = models.TextField(blank=True)
    case_image_alt = models.CharField(max_length=200, default="Business documents and reports on a desk")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Optimize Your Operations?")
    cta_description = models.TextField(default="Let's build systems that work as hard as your team does.")
    cta_button_text = models.CharField(max_length=50, default="Get Started")
    
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Operational Systems Page Content"
        verbose_name_plural = "Operational Systems Page Content"
    
    def __str__(self):
        return f"Operational Systems - {self.hero_title}"


class LivingSystemsPageContent(Audit):
    """Living Systems & Regeneration page content management"""
    
    hero_title = models.CharField(max_length=200, default="Living Systems & Regeneration")
    hero_subtitle = models.TextField(default="Support for land, water, species, and ecosystems — from production systems to restoration and incident response.")
    hero_description = models.TextField(default="We help organizations integrate regenerative practices that benefit both business outcomes and environmental health.")
    hero_image = models.URLField(default="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop")
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Our Regenerative Services")
    service_1_title = models.CharField(max_length=100, default="Ecosystem Restoration")
    service_1_description = models.TextField(default="Restore and regenerate natural systems for long-term sustainability")
    service_2_title = models.CharField(max_length=100, default="Sustainable Production")
    service_2_description = models.TextField(default="Design production systems that work with natural processes")
    service_3_title = models.CharField(max_length=100, default="Environmental Monitoring")
    service_3_description = models.TextField(default="Track and measure environmental impact and recovery")
    
    # Process Section
    process_title = models.CharField(max_length=200, default="Our Regenerative Approach")
    process_description = models.TextField(default="At the heart of our work, we take a systems approach to understanding and regenerating living systems. We observe the current state, design regenerative solutions, and implement systems that restore ecological health while creating economic value.")
    process_step_1 = models.TextField(default="Ecosystem Assessment")
    process_step_2 = models.TextField(default="Regenerative Design")
    process_step_3 = models.TextField(default="Implementation & Monitoring")
    process_step_4 = models.TextField(default="Adaptive Management")
    
    # Case Example Section
    case_challenge = models.TextField(blank=True)
    case_solution = models.TextField(blank=True)
    case_result = models.TextField(blank=True)
    case_image_alt = models.CharField(max_length=200, default="Regenerative agriculture landscape showing restored soil and biodiversity")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Regenerate Your Impact?")
    cta_description = models.TextField(default="Let's create systems that restore while they produce.")
    cta_button_text = models.CharField(max_length=50, default="Get Started")
    
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Living Systems Page Content"
        verbose_name_plural = "Living Systems Page Content"
    
    def __str__(self):
        return f"Living Systems - {self.hero_title}"