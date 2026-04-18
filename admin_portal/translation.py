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

