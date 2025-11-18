from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'phone', 'created_at', 'updated_at')

    list_display_links = ('first_name', 'last_name', 'subject')

    list_filter = ('created_at', 'updated_at')
    
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message', 'phone')
    
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')
