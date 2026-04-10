from rest_framework import serializers
from admin_portal.models_cms import (
    HomePage, ServiceCard, Testimonial, FAQ, BlogPost, 
    ContactInfo, SiteSettings, ApproachSection, BusinessSystemCard,
    BusinessSystemSection, ORRRoleSection, MessageStrip, ProcessStage,
    ProcessSection, ORRReportSection, ServicesPage, ResourcesBlogsPage,
    LegacyPolicyPage, ContactPage
)
from django.core.files.storage import default_storage


class HomePageSerializer(serializers.ModelSerializer):
    """Homepage content serializer"""
    
    class Meta:
        model = HomePage
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'hero_cta_text', 'hero_cta_link',
            'hero_background_image', 'about_title', 'about_content', 'about_image',
            'services_title', 'services_subtitle', 'services_glow_image',
            'service_1_title', 'service_1_description', 'service_1_button',
            'service_2_title', 'service_2_description', 'service_2_button',
            'service_3_title', 'service_3_description', 'service_3_button',
            'contact_title', 'contact_subtitle', 'contact_email', 'contact_phone', 
            'meta_title', 'meta_description', 'is_active', 'last_updated_by', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_updated_by', 'created_at', 'updated_at']


class ServiceCardSerializer(serializers.ModelSerializer):
    """Service card serializer"""
    
    pillar_display = serializers.CharField(source='get_pillar_display', read_only=True)
    
    class Meta:
        model = ServiceCard
        fields = [
            'id', 'title', 'description', 'icon', 'pillar', 'pillar_display',
            'link', 'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TestimonialSerializer(serializers.ModelSerializer):
    """Testimonial serializer"""
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_company', 'client_role', 'testimonial_text',
            'client_photo', 'rating', 'order', 'is_featured', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FAQSerializer(serializers.ModelSerializer):
    """FAQ serializer"""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'category', 'category_display',
            'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BlogPostSerializer(serializers.ModelSerializer):
    """Blog post serializer"""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'author_name', 'status', 'status_display', 'published_at',
            'is_featured', 'meta_title', 'meta_description', 'view_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'view_count', 'created_at', 'updated_at']


class ContactInfoSerializer(serializers.ModelSerializer):
    """Contact information serializer"""
    
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'company_name', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'phone', 'email', 'website',
            'linkedin_url', 'twitter_url', 'facebook_url', 'instagram_url',
            'business_hours', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApproachSectionSerializer(serializers.ModelSerializer):
    """Approach section serializer"""
    
    class Meta:
        model = ApproachSection
        fields = ['id', 'title', 'paragraph_1', 'paragraph_2', 'paragraph_3', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BusinessSystemCardSerializer(serializers.ModelSerializer):
    """Business system card serializer"""
    
    class Meta:
        model = BusinessSystemCard
        fields = ['id', 'title', 'description', 'image', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BusinessSystemSectionSerializer(serializers.ModelSerializer):
    """Business system section serializer"""
    
    # Custom fields to handle both file uploads and URL strings
    card_1_image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    card_2_image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    card_3_image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = BusinessSystemSection
        fields = [
            'id', 'title', 'subtitle', 
            'card_1_title', 'card_1_description', 'card_1_image',
            'card_2_title', 'card_2_description', 'card_2_image',
            'card_3_title', 'card_3_description', 'card_3_image',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """Convert image fields to URLs for frontend"""
        data = super().to_representation(instance)
        
        # Convert image fields to URLs
        if instance.card_1_image:
            data['card_1_image'] = instance.card_1_image.url
        else:
            data['card_1_image'] = '/images/nervous-system.png'
            
        if instance.card_2_image:
            data['card_2_image'] = instance.card_2_image.url
        else:
            data['card_2_image'] = '/images/circulatory-system.png'
            
        if instance.card_3_image:
            data['card_3_image'] = instance.card_3_image.url
        else:
            data['card_3_image'] = '/images/immune-system.png'
            
        return data
    
    def update(self, instance, validated_data):
        """Handle image URL updates"""
        from django.core.files.base import ContentFile
        import os
        
        # Handle image URL updates
        for field_name in ['card_1_image', 'card_2_image', 'card_3_image']:
            if field_name in validated_data:
                image_url = validated_data[field_name]
                
                if image_url and isinstance(image_url, str):
                    if image_url.startswith('/media/'):
                        # It's an uploaded file URL, extract the file path
                        file_path = image_url.replace('/media/', '')
                        # Check if file exists
                        if default_storage.exists(file_path):
                            setattr(instance, field_name, file_path)
                        else:
                            # File doesn't exist, clear the field
                            setattr(instance, field_name, None)
                    elif image_url.startswith('/images/'):
                        # It's a static image, clear the uploaded file field
                        setattr(instance, field_name, None)
                    else:
                        # It's a new uploaded file URL, keep as is
                        # The field should already be set by the upload process
                        pass
                else:
                    # Clear the field if empty
                    setattr(instance, field_name, None)
                
                # Remove from validated_data to avoid conflicts
                validated_data.pop(field_name, None)
        
        # Update other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ORRRoleSectionSerializer(serializers.ModelSerializer):
    """ORR role section serializer"""
    
    class Meta:
        model = ORRRoleSection
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MessageStripSerializer(serializers.ModelSerializer):
    """Message strip serializer"""
    
    class Meta:
        model = MessageStrip
        fields = ['id', 'title', 'message', 'user_image_1', 'user_image_2', 'user_image_3', 'user_image_4', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessStageSerializer(serializers.ModelSerializer):
    """Process stage serializer"""
    
    class Meta:
        model = ProcessStage
        fields = ['id', 'title', 'description', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessSectionSerializer(serializers.ModelSerializer):
    """Process section serializer"""
    
    class Meta:
        model = ProcessSection
        fields = [
            'id', 'title', 'subtitle',
            'stage_1_title', 'stage_1_description',
            'stage_2_title', 'stage_2_description', 
            'stage_3_title', 'stage_3_description',
            'stage_4_title', 'stage_4_description',
            'stage_5_title', 'stage_5_description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ORRReportSectionSerializer(serializers.ModelSerializer):
    """ORR report section serializer"""
    
    class Meta:
        model = ORRReportSection
        fields = [
            'id', 'title', 'subtitle', 'main_image',
            'feature_1', 'feature_1_image',
            'feature_2', 'feature_2_image', 
            'feature_3', 'feature_3_image',
            'feature_4', 'feature_4_image',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServicesPageSerializer(serializers.ModelSerializer):
    """Services page serializer"""
    
    class Meta:
        model = ServicesPage
        fields = [
            'id', 'hero_title', 'hero_subtitle',
            'stage_1_title', 'stage_1_subtitle', 'stage_1_description', 'stage_1_focus', 'stage_1_button_text',
            'stage_2_title', 'stage_2_subtitle', 'stage_2_description', 'stage_2_focus', 'stage_2_button_text',
            'stage_3_title', 'stage_3_subtitle', 'stage_3_description', 'stage_3_focus', 'stage_3_button_1_text', 'stage_3_button_2_text',
            'stage_4_title', 'stage_4_subtitle', 'stage_4_description', 'stage_4_focus', 'stage_4_button_text',
            'stage_5_title', 'stage_5_subtitle', 'stage_5_description', 'stage_5_focus', 'stage_5_button_text',
            'pillars_title',
            'pillar_1_title', 'pillar_1_description', 'pillar_1_button_text',
            'pillar_2_title', 'pillar_2_description', 'pillar_2_button_text',
            'pillar_3_title', 'pillar_3_description', 'pillar_3_button_text',
            'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text', 'business_gp_image',
            'services_overview_title',
            'service_1_title', 'service_1_description', 'service_1_image', 'service_1_button_text',
            'service_2_title', 'service_2_description', 'service_2_image', 'service_2_button_text',
            'data_intelligence_title', 'data_intelligence_description', 'data_intelligence_image', 'data_intelligence_button_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResourcesBlogsPageSerializer(serializers.ModelSerializer):
    """Resources & Blogs page serializer"""
    
    class Meta:
        model = ResourcesBlogsPage
        fields = [
            'id', 'hero_title', 'hero_subtitle',
            'blog_card_1_title', 'blog_card_1_category', 'blog_card_1_image',
            'blog_card_2_title', 'blog_card_2_category', 'blog_card_2_image',
            'blog_card_3_title', 'blog_card_3_category', 'blog_card_3_image',
            'blog_card_4_title', 'blog_card_4_category', 'blog_card_4_image',
            'admin_tips_title',
            'tip_1_number', 'tip_1_title', 'tip_1_description',
            'tip_2_number', 'tip_2_title', 'tip_2_description',
            'tip_3_number', 'tip_3_title', 'tip_3_description',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LegacyPolicyPageSerializer(serializers.ModelSerializer):
    """Legacy & Policy page serializer"""
    
    class Meta:
        model = LegacyPolicyPage
        fields = [
            'id', 'hero_title', 'hero_description',
            'policy_item_1_number', 'policy_item_1_description',
            'policy_item_2_number', 'policy_item_2_description',
            'policy_item_3_number', 'policy_item_3_description',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactPageSerializer(serializers.ModelSerializer):
    """Contact page serializer"""
    
    class Meta:
        model = ContactPage
        fields = [
            'id', 'hero_title',
            'contact_info_title', 'contact_info_subtitle',
            'phone_number', 'email_address', 'address',
            'first_name_label', 'last_name_label', 'email_label', 'phone_label', 'subject_label', 'message_label',
            'first_name_placeholder', 'last_name_placeholder', 'email_placeholder', 'phone_placeholder', 'message_placeholder',
            'subject_option_1', 'subject_option_2', 'subject_option_3', 'subject_option_4',
            'submit_button_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Site settings serializer"""
    
    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_name', 'site_tagline', 'logo', 'favicon',
            'primary_color', 'secondary_color', 'accent_color',
            'footer_text', 'copyright_text', 'google_analytics_id',
            'facebook_pixel_id', 'privacy_policy_url', 'terms_of_service_url',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']