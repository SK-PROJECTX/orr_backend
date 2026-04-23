from modeltranslation.translator import register, TranslationOptions
from .models_cms import (
    HowWeOperatePageContent,
    ProcessStep,
    ServicesPageContent,
    ServiceStage,
    ServicePillar,
    ResourcesBlogsPageContent,
    ContentCard,
    LegalPolicyPageContent,
    PolicyItem,
    ContactPageContent,
    HomePage,
    ServicesPage,
    FAQ,
    ApproachSection,
    BusinessSystemSection,
    ORRRoleSection,
    MessageStrip,
    ProcessSection,
    ORRReportSection,
    ServiceCard,
    Testimonial,
    BlogPost,
    ContactInfo,
    BusinessSystemCard,
    ProcessStage,
    LegacyPolicyPage,
    ContactPage,
    StrategicAdvisoryPageContent,
    OperationalSystemsPageContent,
    LivingSystemsPageContent,
)

@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_subtitle', 'hero_cta_text',
        'about_title', 'about_content',
        'services_title', 'services_subtitle',
        'service_1_title', 'service_1_description', 'service_1_button',
        'service_2_title', 'service_2_description', 'service_2_button',
        'service_3_title', 'service_3_description', 'service_3_button',
        'contact_title', 'contact_subtitle',
        'meta_title', 'meta_description',
    )

@register(HowWeOperatePageContent)
class HowWeOperatePageContentTranslationOptions(TranslationOptions):
    fields = ('hero_title', 'meta_title', 'meta_description')

@register(ProcessStep)
class ProcessStepTranslationOptions(TranslationOptions):
    fields = (
        'title', 'subtitle', 'description', 
        'bullet1', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 
        'bullet6', 'bullet7', 'bullet8', 'bullet9', 
        'wordbreak', 'description1', 'description2', 'description3', 'description4',
        'button_text', 'button_text2', 'button_text3'
    )

@register(ServicesPage)
class ServicesPageTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_subtitle',
        'stage_1_title', 'stage_1_subtitle', 'stage_1_description', 'stage_1_focus', 'stage_1_button_text',
        'stage_2_title', 'stage_2_subtitle', 'stage_2_description', 'stage_2_focus', 'stage_2_button_text',
        'stage_3_title', 'stage_3_subtitle', 'stage_3_description', 'stage_3_focus', 'stage_3_button_1_text', 'stage_3_button_2_text',
        'stage_4_title', 'stage_4_subtitle', 'stage_4_description', 'stage_4_focus', 'stage_4_button_text',
        'stage_5_title', 'stage_5_subtitle', 'stage_5_description', 'stage_5_focus', 'stage_5_button_text',
        'pillars_title',
        'pillar_1_title', 'pillar_1_description', 'pillar_1_button_text',
        'pillar_2_title', 'pillar_2_description', 'pillar_2_button_text',
        'pillar_3_title', 'pillar_3_description', 'pillar_3_button_text',
        'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text',
        'services_overview_title',
        'service_1_title', 'service_1_description', 'service_1_button_text',
        'service_2_title', 'service_2_description', 'service_2_button_text',
        'data_intelligence_title', 'data_intelligence_description', 'data_intelligence_button_text',
        'meta_title', 'meta_description'
    )

@register(ServicesPageContent)
class ServicesPageContentTranslationOptions(TranslationOptions):
    fields = ('hero_title', 'hero_subtitle', 'pillars_title', 'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text', 'meta_title', 'meta_description')

@register(ServiceStage)
class ServiceStageTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'focus_content', 'button_text')

@register(ServicePillar)
class ServicePillarTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'button_text')

@register(ResourcesBlogsPageContent)
class ResourcesBlogsPageContentTranslationOptions(TranslationOptions):
    fields = ('hero_title', 'hero_description1', 'hero_description2', 'hero_description3', 'hero_button1_text', 'hero_button2_text', 'meta_title', 'meta_description')

@register(ContentCard)
class ContentCardTranslationOptions(TranslationOptions):
    fields = ('badge', 'title', 'button1_text', 'button2_text')

@register(LegalPolicyPageContent)
class LegalPolicyPageContentTranslationOptions(TranslationOptions):
    fields = ('hero_title', 'hero_description', 'meta_title', 'meta_description')

@register(PolicyItem)
class PolicyItemTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(ContactPageContent)
class ContactPageContentTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'contact_info_title', 'contact_info_subtitle',
        'first_name_label', 'last_name_label', 'email_label', 'phone_label', 'subject_label', 'message_label',
        'first_name_placeholder', 'last_name_placeholder', 'email_placeholder', 'phone_placeholder', 'message_placeholder',
        'subject_option_1', 'subject_option_2', 'subject_option_3', 'subject_option_4',
        'submit_button_text', 'meta_title', 'meta_description'
    )

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')

@register(ApproachSection)
class ApproachSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'paragraph_1', 'paragraph_2', 'paragraph_3')

@register(BusinessSystemSection)
class BusinessSystemSectionTranslationOptions(TranslationOptions):
    fields = (
        'title', 'subtitle', 
        'card_1_title', 'card_1_description',
        'card_2_title', 'card_2_description',
        'card_3_title', 'card_3_description',
    )

@register(ORRRoleSection)
class ORRRoleSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(MessageStrip)
class MessageStripTranslationOptions(TranslationOptions):
    fields = ('title', 'message')

@register(ProcessSection)
class ProcessSectionTranslationOptions(TranslationOptions):
    fields = (
        'title', 'subtitle',
        'stage_1_title', 'stage_1_description',
        'stage_2_title', 'stage_2_description',
        'stage_3_title', 'stage_3_description',
        'stage_4_title', 'stage_4_description',
        'stage_5_title', 'stage_5_description',
    )

@register(ORRReportSection)
class ORRReportSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'feature_1', 'feature_2', 'feature_3', 'feature_4')

@register(ServiceCard)
class ServiceCardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('client_name', 'client_company', 'client_role', 'testimonial_text')

@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content', 'meta_title', 'meta_description')

@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = (
        'company_name', 'address_line1', 'address_line2', 
        'city', 'state', 'country', 'business_hours',
    )

@register(BusinessSystemCard)
class BusinessSystemCardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(ProcessStage)
class ProcessStageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(LegacyPolicyPage)
class LegacyPolicyPageTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_description',
        'policy_item_1_description', 'policy_item_2_description', 'policy_item_3_description',
        'meta_title', 'meta_description',
    )

@register(ContactPage)
class ContactPageTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'contact_info_title', 'contact_info_subtitle', 'address',
        'first_name_label', 'last_name_label', 'email_label', 'phone_label', 'subject_label', 'message_label',
        'first_name_placeholder', 'last_name_placeholder', 'email_placeholder', 'phone_placeholder', 'message_placeholder',
        'subject_option_1', 'subject_option_2', 'subject_option_3', 'subject_option_4',
        'submit_button_text', 'meta_title', 'meta_description',
    )

@register(StrategicAdvisoryPageContent)
class StrategicAdvisoryPageContentTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_subtitle', 'hero_description',
        'services_title', 'service_1_title', 'service_1_description',
        'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
        'process_title', 'process_subtitle', 'process_description',
        'process_step_1_title', 'process_step_1_subtitle', 'process_step_1',
        'process_step_2_title', 'process_step_2',
        'process_step_3_title', 'process_step_3',
        'process_step_4', 'process_step_4_title',
        'network_title', 'network_description',
        'digital_title', 'digital_subtitle', 'digital_description', 'digital_image_alt',
        'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
        'cta_title', 'cta_description', 'cta_button_text',
        'meta_title', 'meta_description',
    )

@register(OperationalSystemsPageContent)
class OperationalSystemsPageContentTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_subtitle', 'hero_description',
        'services_title', 'service_1_title', 'service_1_description',
        'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
        'process_title', 'process_description',
        'process_step_1_title', 'process_step_1',
        'process_step_2_title', 'process_step_2',
        'process_step_3_title', 'process_step_3',
        'process_step_4_title', 'process_step_4',
        'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
        'cta_title', 'cta_description', 'cta_button_text',
        'meta_title', 'meta_description',
    )

@register(LivingSystemsPageContent)
class LivingSystemsPageContentTranslationOptions(TranslationOptions):
    fields = (
        'hero_title', 'hero_subtitle', 'hero_description',
        'services_title', 'service_1_title', 'service_1_description',
        'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
        'process_title', 'process_description',
        'process_step_1', 'process_step_2', 'process_step_3', 'process_step_4',
        'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
        'cta_title', 'cta_description', 'cta_button_text',
        'meta_title', 'meta_description',
    )

