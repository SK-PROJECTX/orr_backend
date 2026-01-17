from django.db import models
from django import forms
import json


class RichTextFormField(forms.CharField):
    """Form field for rich text content with font size, bold, italic support"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.Textarea(attrs={
            'class': 'rich-text-editor',
            'data-rich-text': 'true'
        }))
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        if not value:
            return value
        
        # If it's already a dict/object, return as is
        if isinstance(value, dict):
            return value
            
        # If it's a string, try to parse as JSON, otherwise treat as plain text
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, treat as plain text and wrap in rich text format
                return {
                    'content': value,
                    'format': 'html'
                }
        
        return value


def _default():
    """Default factory for rich text fields - this function name is what Django looks for"""
    return {'content': '', 'format': 'html'}


def default_rich_text():
    """Default factory for rich text fields"""
    return {'content': '', 'format': 'html'}


def default_rich_text_with_content(content):
    """Factory function for rich text with specific content"""
    def _default():
        return {'content': content, 'format': 'html'}
    return _default


class RichTextField(models.JSONField):
    """
    Custom field for storing rich text content with formatting options.
    Stores content as JSON with format information including font size, bold, italic.
    """
    
    description = "Rich text field with font size, bold, italic support"
    
    def __init__(self, *args, **kwargs):
        # Set default value for rich text using callable
        if 'default' not in kwargs:
            kwargs['default'] = _default
        elif isinstance(kwargs['default'], dict):
            # Convert dict default to callable
            content = kwargs['default'].get('content', '')
            kwargs['default'] = lambda: {'content': content, 'format': 'html'}
        
        super().__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        # Use RichTextFormField and remove form_class from kwargs
        kwargs.pop('form_class', None)
        return RichTextFormField(**kwargs)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        
        # If it's a string, convert to rich text format
        if isinstance(value, str):
            value = {
                'content': value,
                'format': 'html'
            }
        
        return super().get_prep_value(value)
    
    def to_python(self, value):
        if value is None:
            return value
            
        # If it's already processed, return as is
        if isinstance(value, dict):
            return value
            
        # If it's a string, try to parse as JSON
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, treat as plain text
                return {
                    'content': value,
                    'format': 'html'
                }
        
        return super().to_python(value)
    
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if isinstance(value, dict):
            return json.dumps(value)
        return str(value) if value is not None else ''
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure default is properly serializable
        if 'default' in kwargs and callable(kwargs['default']):
            # Replace callable with _default function reference
            kwargs['default'] = _default
        return name, path, args, kwargs


class PlainRichTextField(RichTextField):
    """Rich text field that accepts plain text and converts to rich format"""
    
    def __init__(self, *args, **kwargs):
        # Allow plain text input
        kwargs.setdefault('default', lambda: '')
        super(models.JSONField, self).__init__(*args, **kwargs)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        
        # If it's a plain string, convert to rich text format
        if isinstance(value, str):
            value = {'content': value, 'format': 'html'}
        
        return super().get_prep_value(value)
    
    def to_python(self, value):
        if value is None:
            return value
            
        # If it's already a dict, return as is
        if isinstance(value, dict):
            return value
            
        # If it's a string, try to parse as JSON first
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, treat as plain text
                return {'content': value, 'format': 'html'}
        
        return super().to_python(value)
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Ensure default is properly serializable
        if 'default' in kwargs and callable(kwargs['default']):
            # Replace callable with _default function reference
            kwargs['default'] = _default
        return name, path, args, kwargs