from rest_framework import serializers
from admin_portal.models_cms import (
    # New comprehensive models
    HowWeOperatePageContent, ProcessStep, ServicesPageContent, ServiceStage, ServicePillar,
    ResourcesBlogsPageContent, ContentCard, LegalPolicyPageContent, PolicyItem, ContactPageContent,
    StrategicAdvisoryPageContent, OperationalSystemsPageContent, LivingSystemsPageContent
)


class HowWeOperatePageContentSerializer(serializers.ModelSerializer):
    """How We Operate page content serializer"""
    
    class Meta:
        model = HowWeOperatePageContent
        fields = ['id', 'hero_title', 'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessStepSerializer(serializers.ModelSerializer):
    """Process step serializer"""
    
    class Meta:
        model = ProcessStep
        fields = [
            'id', 'step_number', 'title', 'subtitle', 'description',
            'bullet1', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8', 'bullet9',
            'wordbreak', 'description1', 'description2', 'description3', 'description4',
            'image_url', 'button_text', 'button_text2', 'button_text3', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServicesPageContentSerializer(serializers.ModelSerializer):
    """Services page content serializer"""
    
    class Meta:
        model = ServicesPageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'pillars_title',
            'business_gp_title', 'business_gp_subtitle', 'business_gp_description',
            'business_gp_button_text', 'business_gp_image',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceStageSerializer(serializers.ModelSerializer):
    """Service stage serializer"""
    
    class Meta:
        model = ServiceStage
        fields = [
            'id', 'stage_number', 'title', 'subtitle', 'description',
            'focus_content', 'button_text', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServicePillarSerializer(serializers.ModelSerializer):
    """Service pillar serializer"""
    
    class Meta:
        model = ServicePillar
        fields = [
            'id', 'title', 'description', 'button_text', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResourcesBlogsPageContentSerializer(serializers.ModelSerializer):
    """Resources & Blogs page content serializer"""
    
    class Meta:
        model = ResourcesBlogsPageContent
        fields = [
            'id', 'hero_title', 'hero_description1', 'hero_description2', 'hero_description3',
            'hero_button1_text', 'hero_button2_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContentCardSerializer(serializers.ModelSerializer):
    """Content card serializer"""
    
    class Meta:
        model = ContentCard
        fields = [
            'id', 'badge', 'title', 'card_slug', 'content', 'image_url',
            'button1_text', 'button2_text', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """Validate title field"""
        if isinstance(value, dict) and 'content' in value:
            content = value['content']
            if len(str(content)) > 2000:
                raise serializers.ValidationError("Title content is too long (max 2000 characters)")
        elif isinstance(value, str) and len(value) > 2000:
            raise serializers.ValidationError("Title is too long (max 2000 characters)")
        return value
    
    def validate_badge(self, value):
        """Validate badge field"""
        if isinstance(value, dict) and 'content' in value:
            content = value['content']
            if len(str(content)) > 2000:
                raise serializers.ValidationError("Badge content is too long (max 2000 characters)")
        elif isinstance(value, str) and len(value) > 2000:
            raise serializers.ValidationError("Badge is too long (max 2000 characters)")
        return value
    
    def validate_button1_text(self, value):
        """Validate button1_text field"""
        if isinstance(value, dict) and 'content' in value:
            content = value['content']
            if len(str(content)) > 500:
                raise serializers.ValidationError("Button1 text content is too long (max 500 characters)")
        elif isinstance(value, str) and len(value) > 500:
            raise serializers.ValidationError("Button1 text is too long (max 500 characters)")
        return value
    
    def validate_button2_text(self, value):
        """Validate button2_text field"""
        if isinstance(value, dict) and 'content' in value:
            content = value['content']
            if len(str(content)) > 500:
                raise serializers.ValidationError("Button2 text content is too long (max 500 characters)")
        elif isinstance(value, str) and len(value) > 500:
            raise serializers.ValidationError("Button2 text is too long (max 500 characters)")
        return value
    
    def validate_content(self, value):
        """Validate content array field"""
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str) and len(item) > 5000:
                    raise serializers.ValidationError(f"Content item {i+1} is too long (max 5000 characters)")
        return value
    
    def validate_image_url(self, value):
        """Validate image_url field"""
        if value and len(str(value)) > 500:
            raise serializers.ValidationError("Image URL is too long (max 500 characters)")
        return value


class LegalPolicyPageContentSerializer(serializers.ModelSerializer):
    """Legal & Policy page content serializer"""
    
    class Meta:
        model = LegalPolicyPageContent
        fields = [
            'id', 'hero_title', 'hero_description',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PolicyItemSerializer(serializers.ModelSerializer):
    """Policy item serializer"""
    
    class Meta:
        model = PolicyItem
        fields = [
            'id', 'number', 'description', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactPageContentSerializer(serializers.ModelSerializer):
    """Contact page content serializer"""
    
    class Meta:
        model = ContactPageContent
        fields = [
            'id', 'hero_title', 'contact_info_title', 'contact_info_subtitle',
            'phone_number', 'email_address', 'address',
            'first_name_label', 'last_name_label', 'email_label', 'phone_label',
            'subject_label', 'message_label',
            'first_name_placeholder', 'last_name_placeholder', 'email_placeholder',
            'phone_placeholder', 'message_placeholder',
            'subject_option_1', 'subject_option_2', 'subject_option_3', 'subject_option_4',
            'submit_button_text', 'meta_title', 'meta_description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StrategicAdvisoryPageContentSerializer(serializers.ModelSerializer):
    """Strategic Advisory page content serializer"""
    
    class Meta:
        model = StrategicAdvisoryPageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'hero_description', 'hero_image',
            'services_title', 'service_1_title', 'service_1_description',
            'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
            'process_title', 'process_subtitle', 'process_description',
            'process_step_1_title', 'process_step_1_subtitle', 'process_step_1',
            'process_step_2_title', 'process_step_2', 'process_step_3_title', 'process_step_3',
            'process_step_4', 'process_step_4_title',
            'network_title', 'network_description', 'network_cards',
            'digital_title', 'digital_subtitle', 'digital_description', 'digital_image_alt',
            'digital_who_is_this_for', 'digital_features',
            'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
            'cta_title', 'cta_description', 'cta_button_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OperationalSystemsPageContentSerializer(serializers.ModelSerializer):
    """Operational Systems page content serializer"""
    
    class Meta:
        model = OperationalSystemsPageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'hero_description', 'hero_image',
            'services_title', 'service_1_title', 'service_1_description',
            'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
            'process_title', 'process_description',
            'process_step_1_title', 'process_step_1', 'process_step_2_title', 'process_step_2',
            'process_step_3_title', 'process_step_3',
            'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
            'cta_title', 'cta_description', 'cta_button_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LivingSystemsPageContentSerializer(serializers.ModelSerializer):
    """Living Systems page content serializer"""
    
    class Meta:
        model = LivingSystemsPageContent
        fields = [
            'id', 'hero_title', 'hero_subtitle', 'hero_description', 'hero_image',
            'services_title', 'service_1_title', 'service_1_description',
            'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description',
            'process_title', 'process_description',
            'process_step_1', 'process_step_2', 'process_step_3', 'process_step_4',
            'case_challenge', 'case_solution', 'case_result', 'case_image_alt',
            'cta_title', 'cta_description', 'cta_button_text',
            'meta_title', 'meta_description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']