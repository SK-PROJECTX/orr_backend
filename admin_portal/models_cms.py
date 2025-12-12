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