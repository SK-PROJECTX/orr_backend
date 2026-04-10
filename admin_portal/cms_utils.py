"""
CMS Validation Utilities

This module provides validation functions and error handling for CMS operations
to prevent varchar(50) and other database constraint errors.
"""

import json
from typing import Any, Dict, List, Tuple, Union
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError


class CMSValidationError(Exception):
    """Custom exception for CMS validation errors"""
    pass


class CMSFieldValidator:
    """Validator for CMS fields to prevent database constraint errors"""
    
    # Field length limits
    FIELD_LIMITS = {
        'rich_text_content': 2000,
        'rich_text_short': 500,
        'url_field': 500,
        'slug_field': 500,
        'char_field': 500,
        'text_content': 5000,
    }
    
    @classmethod
    def validate_rich_text_field(cls, value: Any, field_name: str, max_length: int = None) -> Any:
        """Validate RichTextField content"""
        if max_length is None:
            max_length = cls.FIELD_LIMITS['rich_text_content']
        
        if value is None:
            return value
        
        if isinstance(value, dict):
            if 'content' in value:
                content = str(value['content'])
                if len(content) > max_length:
                    raise CMSValidationError(
                        f"{field_name} content is too long ({len(content)} chars, max {max_length})"
                    )
            return value
        
        elif isinstance(value, str):
            if len(value) > max_length:
                raise CMSValidationError(
                    f"{field_name} is too long ({len(value)} chars, max {max_length})"
                )
            # Convert string to rich text format
            return {'content': value, 'format': 'html'}
        
        return value
    
    @classmethod
    def validate_url_field(cls, value: str, field_name: str) -> str:
        """Validate URL field length"""
        if value and len(str(value)) > cls.FIELD_LIMITS['url_field']:
            raise CMSValidationError(
                f"{field_name} URL is too long ({len(str(value))} chars, max {cls.FIELD_LIMITS['url_field']})"
            )
        return value
    
    @classmethod
    def validate_char_field(cls, value: str, field_name: str, max_length: int = None) -> str:
        """Validate CharField length"""
        if max_length is None:
            max_length = cls.FIELD_LIMITS['char_field']
        
        if value and len(str(value)) > max_length:
            raise CMSValidationError(
                f"{field_name} is too long ({len(str(value))} chars, max {max_length})"
            )
        return value
    
    @classmethod
    def validate_content_array(cls, value: List[str], field_name: str) -> List[str]:
        """Validate content array field"""
        if not isinstance(value, list):
            return value
        
        max_length = cls.FIELD_LIMITS['text_content']
        for i, item in enumerate(value):
            if isinstance(item, str) and len(item) > max_length:
                raise CMSValidationError(
                    f"{field_name} item {i+1} is too long ({len(item)} chars, max {max_length})"
                )
        return value
    
    @classmethod
    def validate_content_card_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate ContentCard data comprehensively"""
        validated_data = data.copy()
        
        # Validate RichTextField fields
        rich_text_fields = ['badge', 'title', 'button1_text', 'button2_text']
        for field in rich_text_fields:
            if field in validated_data:
                max_len = cls.FIELD_LIMITS['rich_text_short'] if 'button' in field else cls.FIELD_LIMITS['rich_text_content']
                validated_data[field] = cls.validate_rich_text_field(
                    validated_data[field], field, max_len
                )
        
        # Validate URL field
        if 'image_url' in validated_data:
            validated_data['image_url'] = cls.validate_url_field(
                validated_data['image_url'], 'image_url'
            )
        
        # Validate content array
        if 'content' in validated_data:
            validated_data['content'] = cls.validate_content_array(
                validated_data['content'], 'content'
            )
        
        # Validate slug field
        if 'card_slug' in validated_data:
            validated_data['card_slug'] = cls.validate_char_field(
                validated_data['card_slug'], 'card_slug', cls.FIELD_LIMITS['slug_field']
            )
        
        return validated_data


class CMSErrorHandler:
    """Error handler for CMS operations"""
    
    @staticmethod
    def handle_database_error(error: Exception, operation: str = "operation") -> Dict[str, Any]:
        """Handle database errors and return appropriate response"""
        
        if isinstance(error, DataError):
            error_msg = str(error)
            
            # Check for varchar constraint errors
            if "value too long for type character varying" in error_msg:
                if "character varying(50)" in error_msg:
                    return {
                        'success': False,
                        'status': 400,
                        'message': 'Error updating content: Field content is too long. Please reduce the text length and try again.',
                        'data': {
                            'error_type': 'field_too_long',
                            'suggestion': 'Reduce the length of your content and try again.'
                        }
                    }
                else:
                    return {
                        'success': False,
                        'status': 400,
                        'message': 'Error updating content: One or more fields exceed the maximum allowed length.',
                        'data': {
                            'error_type': 'field_too_long',
                            'suggestion': 'Please check your content length and try again.'
                        }
                    }
        
        elif isinstance(error, IntegrityError):
            error_msg = str(error)
            
            if "duplicate key value" in error_msg:
                return {
                    'success': False,
                    'status': 400,
                    'message': 'Error updating content: Duplicate value detected.',
                    'data': {
                        'error_type': 'duplicate_value',
                        'suggestion': 'Please use a unique value and try again.'
                    }
                }
        
        elif isinstance(error, CMSValidationError):
            return {
                'success': False,
                'status': 400,
                'message': f'Validation error: {str(error)}',
                'data': {
                    'error_type': 'validation_error',
                    'suggestion': 'Please check your input and try again.'
                }
            }
        
        # Generic error handling
        return {
            'success': False,
            'status': 500,
            'message': f'Error during {operation}: {str(error)}',
            'data': {
                'error_type': 'server_error',
                'suggestion': 'Please try again later or contact support if the issue persists.'
            }
        }
    
    @staticmethod
    def safe_cms_operation(operation_func, *args, **kwargs) -> Dict[str, Any]:
        """Safely execute a CMS operation with error handling"""
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            return CMSErrorHandler.handle_database_error(e, operation_func.__name__)


def truncate_field_content(value: Any, max_length: int, field_name: str = "field") -> Any:
    """Safely truncate field content to fit database constraints"""
    
    if value is None:
        return value
    
    if isinstance(value, dict) and 'content' in value:
        content = str(value['content'])
        if len(content) > max_length:
            value['content'] = content[:max_length-3] + '...'
        return value
    
    elif isinstance(value, str):
        if len(value) > max_length:
            return value[:max_length-3] + '...'
        return value
    
    elif isinstance(value, list):
        # Handle content arrays
        truncated_list = []
        for item in value:
            if isinstance(item, str) and len(item) > max_length:
                truncated_list.append(item[:max_length-3] + '...')
            else:
                truncated_list.append(item)
        return truncated_list
    
    return value


def validate_and_clean_cms_data(data: Dict[str, Any], model_type: str = "generic") -> Dict[str, Any]:
    """Validate and clean CMS data before saving"""
    
    if model_type == "content_card":
        return CMSFieldValidator.validate_content_card_data(data)
    
    # Generic validation for other CMS models
    cleaned_data = {}
    
    for field_name, value in data.items():
        try:
            if field_name.endswith('_url') or field_name == 'image_url':
                cleaned_data[field_name] = CMSFieldValidator.validate_url_field(value, field_name)
            elif field_name in ['title', 'subtitle', 'description', 'content']:
                cleaned_data[field_name] = CMSFieldValidator.validate_rich_text_field(value, field_name)
            elif field_name.endswith('_slug') or field_name == 'slug':
                cleaned_data[field_name] = CMSFieldValidator.validate_char_field(value, field_name, 500)
            else:
                cleaned_data[field_name] = value
        except CMSValidationError:
            # If validation fails, truncate the content
            if isinstance(value, (str, dict, list)):
                cleaned_data[field_name] = truncate_field_content(value, 500, field_name)
            else:
                cleaned_data[field_name] = value
    
    return cleaned_data