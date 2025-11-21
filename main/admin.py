from django.contrib import admin
from .models import BlogPost, AnalyticsCaseStudy, IndustryInsight, ContactMessage

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'published_at')
    list_filter = ('category', 'is_featured', 'published_at')
    search_fields = ('title', 'excerpt', 'content', 'category')
    prepopulated_fields = {'slug': ('title',)}  
    ordering = ('-published_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AnalyticsCaseStudy)
class AnalyticsCaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'active_users', 'questions_answered', 'avg_session_length', 'knowledge_gain')
    search_fields = ('title',)
    readonly_fields = ('starting_knowledge', 'current_knowledge', 'knowledge_gain')


@admin.register(IndustryInsight)
class IndustryInsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'real_time_users', 'total_visits', 'visit_duration')
    search_fields = ('title',)
    readonly_fields = ('top_countries', 'engagement_data', 'created_at', 'updated_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'phone', 'created_at', 'updated_at')

    list_display_links = ('first_name', 'last_name', 'subject')

    list_filter = ('created_at', 'updated_at')
    
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message', 'phone')
    
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')