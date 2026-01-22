#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
django.setup()

from admin_portal.models_cms import (
    HowWeOperatePageContent, ProcessStep, ServicesPageContent, ServiceStage, ServicePillar,
    ResourcesBlogsPageContent, ContentCard, LegalPolicyPageContent, PolicyItem, ContactPageContent
)

def create_how_we_operate_data():
    """Create How We Operate page data"""
    page, created = HowWeOperatePageContent.objects.update_or_create(
        is_active=True,
        defaults={'hero_title': 'How We Operate'}
    )
    
    # Create 10 process steps with the current frontend data
    steps_data = [
        {
            'step_number': '01',
            'title': 'The Beginning',
            'bullet1': 'A quiet conversation.',
            'bullet2': 'One problem.',
            'bullet3': 'One pressure point.',
            'bullet4': 'One story that finally gets told.',
            'description1': 'We listen. Properly.',
            'description2': 'Not to diagnose too fast, not to impress —',
            'description3': 'but to understand how your organisation actually breathes.',
            'description4': 'As you scroll, the screen lights up with your world: the systems you built, the gaps you tolerate, the ideas you haven\'t voiced yet.',
            'image_url': 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=600&fit=crop',
            'order': 1
        },
        {
            'step_number': '02',
            'title': 'The First Map',
            'subtitle': 'After the meeting, the noise clears.',
            'description': 'We open a blank page and begin drawing the first map of your organisation: where things flow, where they clog, where hidden energy leaks.',
            'bullet1': 'No polish.',
            'bullet2': 'No sales pitch.',
            'bullet3': 'Just thinking in writing — your case file begins here.',
            'description1': 'This becomes the backbone of everything that follows.',
            'image_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=600&fit=crop',
            'order': 2
        },
        {
            'step_number': '03',
            'title': 'The Deepening',
            'subtitle': 'The map sharpens.',
            'description': 'We pull in the right forms of intelligence: domain insight, targeted research, regulatory skeletons, operational patterns, AI opportunities, risk shadows.',
            'bullet1': 'Only what adds value.',
            'bullet2': 'No sales pitch.',
            'bullet3': 'Nothing that inflates the process.',
            'description1': 'Your world becomes clearer, not bigger.',
            'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop',
            'order': 3
        },
        {
            'step_number': '04',
            'title': 'The Second Conversation',
            'subtitle': 'Now the questions get sharper.',
            'bullet1': 'We return to you — briefly, precisely.',
            'bullet2': 'To test assumptions.',
            'bullet3': 'To correct tone.',
            'bullet4': 'To realign the map with the reality you inhabit.',
            'description1': 'This is where the document stops being analysis and starts becoming a design for action.',
            'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop',
            'order': 4
        },
        {
            'step_number': '05',
            'title': 'The ORR Report',
            'subtitle': 'You reach the decision point.',
            'description': 'What you receive is not decoration — but a structured, decision-ready model:',
            'bullet1': 'What is happening.',
            'bullet2': 'Why it\'s happening.',
            'bullet3': 'What must change now.',
            'bullet4': 'What can grow later.',
            'bullet5': 'And a modus operandi that ties it all together.',
            'description1': 'A blueprint that stands on its own. With us, or without us.',
            'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
            'order': 5
        },
        {
            'step_number': '06',
            'title': 'The Meeting Architecture',
            'subtitle': 'Behind the scenes, the rhythm is simple:',
            'description': 'First Meeting → Discovery → Follow-Up → Report Review',
            'bullet1': 'Each one short.',
            'bullet2': 'Each one deliberate.',
            'bullet3': 'Each one designed to move the case forward, never sideways.',
            'description1': 'This cadence keeps the process light, while the thinking stays deep.',
            'image_url': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=600&fit=crop',
            'order': 6
        },
        {
            'step_number': '07',
            'title': 'The Choice',
            'subtitle': 'With the report in hand, you choose the path:',
            'bullet1': 'Stop here.',
            'bullet2': 'Use the blueprint internally.',
            'wordbreak': 'OR',
            'bullet3': 'Continue.',
            'bullet4': 'Let ORR coordinate implementation,',
            'bullet5': 'structure your systems,',
            'bullet6': 'refine your operations,',
            'bullet7': 'and support your growth through a sustained relationship.',
            'description1': 'Either way:',
            'description2': 'you walk away with clarity.',
            'image_url': 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800&h=600&fit=crop',
            'order': 7
        },
        {
            'step_number': '08',
            'title': 'The Portal',
            'subtitle': 'If you stay with us, the work shifts into a different gear.',
            'description': 'The Client Portal unlocks:',
            'bullet1': 'your meetings,',
            'bullet2': 'your documents,',
            'bullet3': 'your tasks,',
            'bullet4': 'your insights,',
            'bullet5': 'your Workspace.',
            'bullet8': 'One interface.',
            'bullet9': 'No scattered emails',
            'description2': 'A single coordination layer for your ongoing transformation.',
            'image_url': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=600&fit=crop',
            'order': 8
        },
        {
            'step_number': '09',
            'title': 'The Philosophy Underneath',
            'subtitle': 'At every step, the model holds:',
            'description': 'Discover → Diagnose → Design → Deploy → Grow',
            'description1': 'It is the Business GP method — the quiet, structured way to stabilise an organisation and then help it operate like a living system:',
            'description2': 'coherent, adaptive, responsive.',
            'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&h=600&fit=crop',
            'order': 9
        },
        {
            'step_number': '10',
            'title': 'The Invitation',
            'subtitle': 'If this approach feels different, it\'s because it is.',
            'description1': 'It is slower at the beginning, faster at the end, and clearer all the way through.',
            'description2': 'Start with one meeting. The rest unfolds from there.',
            'image_url': 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&h=600&fit=crop',
            'button_text': 'Book Your First Meeting',
            'button_text2': 'Explore our services',
            'button_text3': 'Access the Client Portal',
            'order': 10
        }
    ]
    
    for step_data in steps_data:
        ProcessStep.objects.update_or_create(
            step_number=step_data['step_number'],
            defaults=step_data
        )
    
    print("✓ How We Operate page data created")

def create_services_page_data():
    """Create Services page data"""
    page, created = ServicesPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'ORR Solutions - Listen. Solve. Optimise.',
            'hero_subtitle': 'We treat your organisation as a whole system — digital, regulatory, and living. We listen first, then design the right mix of advisory, systems, AI, and on-the-ground projects so you can move better and grow smarter too.',
            'pillars_title': 'The Three Pillars',
            'business_gp_title': 'ORR is your Business GP for',
            'business_gp_subtitle': 'complex systems — digital and living.',
            'business_gp_description': 'We listen to the whole organisation, solve with structure and insight, and optimise so you can grow with confidence.',
            'business_gp_button_text': 'Contact Us',
            'business_gp_image': '/images/handshake.png'
        }
    )
    
    # Create service stages
    stages_data = [
        {
            'stage_number': 1,
            'title': 'STAGE 1 - DISCOVER',
            'subtitle': 'Listen.',
            'description': 'We start simple: one calm conversation and a quick scan of your reality.',
            'focus_content': 'We focus on:\n• Your context, people, and pressures\n• Regulatory, operational, data, and environmental risks\n• Which questions actually matter',
            'button_text': 'Sign up',
            'order': 1
        },
        {
            'stage_number': 2,
            'title': 'STAGE 2 - DIAGNOSE',
            'subtitle': 'Think. Then listen again.',
            'description': 'We turn symptoms into a clear map of problems and opportunities across three pillars.',
            'focus_content': 'What happens here:\n• Bottleneck and process mapping\n• Compliance, governance, and risk review\n• Data and living systems scan\n• Prioritised list: urgent, high leverage, later',
            'button_text': 'Learn More',
            'order': 2
        },
        {
            'stage_number': 3,
            'title': 'STAGE 3 - DESIGN',
            'subtitle': 'Design.',
            'description': 'We design practical structures not theory decks.',
            'focus_content': 'Typical Outputs:\n• SOPs and standardised workflows\n• Communication and decision pathways\n• Tech stacks, integration and AI use-case\n• Simple concepts for field or nurture projects\n• Clean, structured data ready for reporting',
            'button_text': 'Sign up',
            'order': 3
        },
        {
            'stage_number': 4,
            'title': 'STAGE 4 - DEPLOY',
            'subtitle': 'Solve in practice.',
            'description': 'Design becomes reality with guided implementation.',
            'focus_content': 'Deployment can include:\n• Admin and records setup\n• Client logging, pipeline, and follow-up flows\n• KPI fit dashboards with AI summaries\n• Staff training in the tools you already use\n• Connecting with external providers where needed',
            'button_text': 'Contact Us',
            'order': 4
        },
        {
            'stage_number': 5,
            'title': 'STAGE 5 - GROW',
            'subtitle': 'Optimise.',
            'description': 'Once systems are live, we keep them learning.',
            'focus_content': 'How we support growth:\n• Ongoing data capture and light analytics\n• Quarterly reviews and system tuning\n• AI-assisted monitoring and early warnings\n• Scenario and \'what if\' thinking\n• Light, regular check-ins — your systems clinic',
            'button_text': 'Sign up',
            'order': 5
        }
    ]
    ServiceStage.objects.all().delete()
    for stage_data in stages_data:
        ServiceStage.objects.update_or_create(
            stage_number=stage_data['stage_number'],
            defaults=stage_data
        )
    
    # Create service pillars
    pillars_data = [
        {
            'title': 'Digital Systems, Automation & AI',
            'description': 'SOPs, workflows, portals, dashboards, and AI helpers that make work flow with less effort and fewer surprises.',
            'button_text': 'Learn More',
            'order': 1
        },
        {
            'title': 'Strategic Advisory & Compliance',
            'description': 'Short, sharp clarity on rules, risk, and direction — from regulation and ESG to biotech and environmental questions.',
            'button_text': 'Learn More',
            'order': 2
        },
        {
            'title': 'Living Systems & Regeneration',
            'description': 'Support for land, water, species, and ecosystems — from production systems to restoration and incident response.',
            'button_text': 'Learn More',
            'order': 3
        }
    ]
    
    for pillar_data in pillars_data:
        ServicePillar.objects.update_or_create(
            title=pillar_data['title'],
            defaults=pillar_data
        )
    
    print("✓ Services page data created")

def create_resources_page_data():
    """Create Resources & Blogs page data"""
    page, created = ResourcesBlogsPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Resources & Client Portal',
            'hero_description1': 'Your digital HQ for business clarity, timelines, and real-time status. This isn\'t a traditional blog.',
            'hero_description2': 'Our resources are organized around the ORR client portal — a dashboard where you can read FAQs, download material, request meetings, and chat with a live operator or consultant.',
            'hero_description3': 'Instead of scattered articles, you get structured guidance that follows our live project — following blogs have insight, how-to — and real-time alerts. Everything is organized around live project management, AI marketing systems & implementation.',
            'hero_button1_text': 'Request access to the client portal',
            'hero_button2_text': 'Learn how we operate'
        }
    )
    
    # Create content cards
    cards_data = [
        {
            'badge': 'Blog',
            'title': 'WHY A PORTAL, NOT JUST A BLOG?',
            'content': [
                'Designed for people who want to act, not just read.',
                'Everything you need is one location.',
                'Live ORR client portal connects resources, FAQs, chat, and project management in one place.',
                'Questions or decisions can be live chat with consultants.',
                'Sharing links, documents, and project updates happens in real-time.',
                'Sharing FAQs',
                'Everything you need to know about how we work and the projects we deliver is in one place.',
                'Project workflow is dynamic.'
            ],
            'image_url': 'https://res.cloudinary.com/depeqzb6z/image/upload/v1765559589/21743692_6495306_uay57y.jpg',
            'order': 1
        },
        {
            'badge': 'Guide',
            'title': 'HOW CONTENT IS ORGANISED',
            'content': [
                'Resources that follow the way we work.',
                'Everything here is project-focused live resources — not standalone articles or random tips.',
                'By Stage:',
                '• Discovery — understand, feedback, and next steps',
                '• Define — deliverables, timelines, and expectations',
                '• Deploy — live development, testing, and launch',
                '• Deliver — handover, training, and ongoing support',
                'By Type:',
                '• FAQs — quick answers to common questions',
                '• Guides — step-by-step processes for clients, stakeholders, and change management',
                '• Resources — templates, checklists, and tools',
                '• Updates — real-time project status, new features, and announcements'
            ],
            'image_url': 'https://res.cloudinary.com/depeqzb6z/image/upload/v1765559588/11235559_10793_z44m6j.jpg',
            'order': 2
        },
        {
            'badge': 'Guide',
            'title': 'WHAT YOU CAN DO TODAY',
            'content': [
                'Before, during, and after working with ORR.',
                'Whether you\'re just starting or already — or just thinking about it:',
                'Read our FAQ and request a call with us.',
                'Before you engage:',
                'Read how our live meeting and client work happens — so you know what to expect when we start working together.',
                'During engagement:',
                'Access live project status in real-time — see progress, ask questions, and get immediate answers from our team.',
                'After project is complete:',
                'Download resources from completed work, get ongoing support, and access to our alumni network.',
                'Access resources on key development, project management, and business growth topics.'
            ],
            'image_url': 'https://res.cloudinary.com/depeqzb6z/image/upload/v1765559588/12146019_Wavy_Gen-02_Single-01_xkhifo.jpg',
            'order': 3
        },
        {
            'badge': 'Access',
            'title': 'HOW ACCESS WORKS',
            'content': [
                'Simple. Immediate access.',
                'Request access:',
                'Click above button and we\'ll send you an email with your login details.',
                'Receive your login:',
                'Check your email for credentials and the link to your client portal.',
                'Start exploring:',
                'Log in and start exploring resources, FAQs, and project tools.',
                'Book your first chat:',
                'Use our in-app calendar to book a 15-minute call with our team to discuss your project and next steps.',
                'Request your first project:',
                'Submit your first project request directly through the portal and begin our 4-stage process.'
            ],
            'image_url': 'https://res.cloudinary.com/depeqzb6z/image/upload/v1765559586/133742375_10241279_mghczg.jpg',
            'button1_text': 'Request access to the client portal',
            'button2_text': 'Learn how we operate',
            'order': 4
        }
    ]
    
    for card_data in cards_data:
        ContentCard.objects.update_or_create(
    title=card_data['title'],
    defaults={
        'card_slug': card_data.get('card_slug', card_data['title'].replace(' ', '-').lower()),
        **card_data
    }
)


    
    print("✓ Resources & Blogs page data created")

def create_legal_policy_data():
    """Create Legal & Policy page data"""
    page, created = LegalPolicyPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Legacy & Policy',
            'hero_description': 'Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.'
        }
    )
    
    # Create policy items
    items_data = [
        {
            'number': '01',
            'description': 'Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.',
            'order': 1
        },
        {
            'number': '02',
            'description': 'Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.',
            'order': 2
        },
        {
            'number': '03',
            'description': 'Lorem ipsm jgdu mplexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving legal, scientific, and operational standards. Our approach combines deep technical insight with strategic foresight — ensuring every initiative is compliant, sustainable, and built for growth.',
            'order': 3
        }
    ]
    
    for item_data in items_data:
        PolicyItem.objects.update_or_create(
            number=item_data['number'],
            defaults=item_data
        )
    
    print("✓ Legal & Policy page data created")

def create_contact_page_data():
    """Create Contact page data"""
    # First, deactivate any existing active records
    ContactPageContent.objects.filter(is_active=True).update(is_active=False)
    
    # Then create or get the single active record
    page, created = ContactPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Contact Us',
            'contact_info_title': 'Contact Information',
            'contact_info_subtitle': 'Say something to start a live chat!',
            'phone_number': '+012 3456 789',
            'email_address': 'demo@gmail.com',
            'address': '132 Dartmouth Street Boston, Massachusetts 02156 United States',
            'first_name_label': 'First Name',
            'last_name_label': 'Last Name',
            'email_label': 'Email',
            'phone_label': 'Phone Number',
            'subject_label': 'Select Subject?',
            'message_label': 'Message',
            'first_name_placeholder': 'John',
            'last_name_placeholder': 'Doe',
            'email_placeholder': 'your@email.com',
            'phone_placeholder': '+1 012 3456 789',
            'message_placeholder': 'Write your message...',
            'subject_option_1': 'General Inquiry',
            'subject_option_2': 'General Inquiry',
            'subject_option_3': 'General Inquiry',
            'subject_option_4': 'General Inquiry',
            'submit_button_text': 'Send Message'
        }
    )
    
    print("✓ Contact page data created")

if __name__ == '__main__':
    print("Creating comprehensive CMS seed data...")
    create_how_we_operate_data()
    create_services_page_data()
    create_resources_page_data()
    create_legal_policy_data()
    create_contact_page_data()
    print("✅ All CMS seed data created successfully!")