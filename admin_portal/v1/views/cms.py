from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import uuid
import os

from admin_portal.permissions import CanCreateContent, CanPublishContent
from admin_portal.models_cms import (
    HomePage, ServiceCard, Testimonial, FAQ, BlogPost, 
    ContactInfo, SiteSettings, ApproachSection, BusinessSystemSection,
    ORRRoleSection, MessageStrip, ProcessSection, ORRReportSection
)
from ..serializers.cms import (
    HomePageSerializer, ServiceCardSerializer, TestimonialSerializer,
    FAQSerializer, BlogPostSerializer, ContactInfoSerializer, SiteSettingsSerializer,
    ApproachSectionSerializer, BusinessSystemSectionSerializer, ORRRoleSectionSerializer,
    MessageStripSerializer, ProcessSectionSerializer, ORRReportSectionSerializer
)


@extend_schema(
    tags=["CMS - Homepage"],
    summary="Get or update homepage content",
    description="Manage homepage hero section, about section, and other content blocks."
)
@method_decorator(csrf_exempt, name='dispatch')
class HomePageView(APIView):
    """Homepage content management"""
    
    def get_permissions(self):
        # Allow all requests for now to test functionality
        return []
    
    def get(self, request):
        homepage, created = HomePage.objects.get_or_create(
            is_active=True,
            defaults={'hero_title': 'Transform Your Business with ORR'}
        )
        serializer = HomePageSerializer(homepage)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Request successful',
            'data': serializer.data
        })
    
    def put(self, request):
        homepage, created = HomePage.objects.get_or_create(is_active=True)
        serializer = HomePageSerializer(homepage, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Only set last_updated_by if user is authenticated
            if request.user.is_authenticated:
                serializer.save(last_updated_by=request.user)
            else:
                serializer.save()
            return Response({
                'success': True,
                'status': 200,
                'message': 'Homepage updated successfully',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'status': 400,
            'message': 'Validation failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Services"],
    summary="List or create service cards",
    description="Manage service cards displayed on homepage."
)
class ServiceCardListView(generics.ListCreateAPIView):
    """Service cards management"""
    queryset = ServiceCard.objects.filter(is_active=True)
    serializer_class = ServiceCardSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [CanCreateContent()]
    
    def perform_create(self, serializer):
        serializer.save()


@extend_schema(
    tags=["CMS - Services"],
    summary="Update or delete service card",
    description="Manage individual service cards."
)
class ServiceCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Individual service card management"""
    queryset = ServiceCard.objects.all()
    serializer_class = ServiceCardSerializer
    permission_classes = [CanCreateContent]


@extend_schema(
    tags=["CMS - Testimonials"],
    summary="List or create testimonials",
    description="Manage client testimonials for homepage."
)
class TestimonialListView(generics.ListCreateAPIView):
    """Testimonials management"""
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    permission_classes = [CanCreateContent]


@extend_schema(
    tags=["CMS - Testimonials"],
    summary="Update or delete testimonial",
    description="Manage individual testimonials."
)
class TestimonialDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Individual testimonial management"""
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [CanCreateContent]


@extend_schema(
    tags=["CMS - FAQ"],
    summary="List or create FAQs",
    description="Manage frequently asked questions by category."
)
class FAQListView(generics.ListCreateAPIView):
    """FAQ management"""
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [CanCreateContent()]
    
    def get_queryset(self):
        queryset = FAQ.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


@extend_schema(
    tags=["CMS - FAQ"],
    summary="Update or delete FAQ",
    description="Manage individual FAQ items."
)
class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Individual FAQ management"""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            return []
        return [CanCreateContent()]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(
    tags=["CMS - Blog"],
    summary="List or create blog posts",
    description="Manage blog posts for homepage and blog section."
)
class BlogPostListView(generics.ListCreateAPIView):
    """Blog posts management"""
    serializer_class = BlogPostSerializer
    permission_classes = [CanCreateContent]
    
    def get_queryset(self):
        queryset = BlogPost.objects.all()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    def perform_create(self, serializer):
        if not serializer.validated_data.get('slug'):
            serializer.validated_data['slug'] = slugify(serializer.validated_data['title'])
        serializer.save(author=self.request.user)


@extend_schema(
    tags=["CMS - Blog"],
    summary="Update or delete blog post",
    description="Manage individual blog posts."
)
class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Individual blog post management"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [CanCreateContent]


@extend_schema(
    tags=["CMS - Blog"],
    summary="Publish blog post",
    description="Publish or unpublish blog posts."
)
class BlogPostPublishView(APIView):
    """Blog post publishing"""
    permission_classes = [CanPublishContent]
    
    def post(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
            action = request.data.get('action', 'publish')
            
            if action == 'publish':
                blog_post.status = 'published'
                from django.utils import timezone
                blog_post.published_at = timezone.now()
            elif action == 'unpublish':
                blog_post.status = 'draft'
                blog_post.published_at = None
            
            blog_post.save()
            
            return Response({
                'message': f'Blog post {action}ed successfully',
                'status': blog_post.status
            })
            
        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Blog post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["CMS - Contact"],
    summary="Get or update contact information",
    description="Manage company contact information and social media links."
)
class ContactInfoView(APIView):
    """Contact information management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        contact_info, created = ContactInfo.objects.get_or_create(
            is_active=True,
            defaults={'company_name': 'ORR', 'email': 'info@orr.com'}
        )
        serializer = ContactInfoSerializer(contact_info)
        return Response(serializer.data)
    
    def put(self, request):
        contact_info, created = ContactInfo.objects.get_or_create(is_active=True)
        serializer = ContactInfoSerializer(contact_info, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Settings"],
    summary="Get or update site settings",
    description="Manage global site settings including branding, colors, and analytics."
)
class SiteSettingsView(APIView):
    """Site settings management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        settings, created = SiteSettings.objects.get_or_create(
            is_active=True,
            defaults={'site_name': 'ORR'}
        )
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)
    
    def put(self, request):
        settings, created = SiteSettings.objects.get_or_create(is_active=True)
        serializer = SiteSettingsSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Approach"],
    summary="Get or update approach section",
    description="Manage approach section content."
)
@method_decorator(csrf_exempt, name='dispatch')
class ApproachSectionView(APIView):
    """Approach section management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        approach, created = ApproachSection.objects.get_or_create(is_active=True)
        serializer = ApproachSectionSerializer(approach)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Request successful',
            'data': serializer.data
        })
    
    def put(self, request):
        approach, created = ApproachSection.objects.get_or_create(is_active=True)
        serializer = ApproachSectionSerializer(approach, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Business System"],
    summary="Get or update business system section",
    description="Manage business system section content."
)
@method_decorator(csrf_exempt, name='dispatch')
class BusinessSystemSectionView(APIView):
    """Business system section management"""
    
    def get_permissions(self):
        # Allow GET requests without authentication, require auth for PUT
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated()]
    
    def get(self, request):
        section, created = BusinessSystemSection.objects.get_or_create(is_active=True)
        serializer = BusinessSystemSectionSerializer(section)
        return Response({
            'success': True,
            'status': 200,
            'message': 'Request successful',
            'data': serializer.data
        })
    
    def put(self, request):
        try:
            section, created = BusinessSystemSection.objects.get_or_create(is_active=True)
            serializer = BusinessSystemSectionSerializer(section, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Only set last_updated_by if user is authenticated
                if request.user.is_authenticated:
                    serializer.save(last_updated_by=request.user)
                else:
                    serializer.save()
                return Response({
                    'success': True,
                    'status': 200,
                    'message': 'Business system section updated successfully',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'status': 400,
                'message': 'Validation failed',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'status': 500,
                'message': f'Server error: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=["CMS - ORR Role"],
    summary="Get or update ORR role section",
    description="Manage ORR role section content."
)
@method_decorator(csrf_exempt, name='dispatch')
class ORRRoleSectionView(APIView):
    """ORR role section management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        section, created = ORRRoleSection.objects.get_or_create(is_active=True)
        serializer = ORRRoleSectionSerializer(section)
        return Response(serializer.data)
    
    def put(self, request):
        section, created = ORRRoleSection.objects.get_or_create(is_active=True)
        serializer = ORRRoleSectionSerializer(section, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Message Strip"],
    summary="Get or update message strip",
    description="Manage message strip content."
)
@method_decorator(csrf_exempt, name='dispatch')
class MessageStripView(APIView):
    """Message strip management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        strip, created = MessageStrip.objects.get_or_create(is_active=True)
        serializer = MessageStripSerializer(strip)
        return Response(serializer.data)
    
    def put(self, request):
        strip, created = MessageStrip.objects.get_or_create(is_active=True)
        serializer = MessageStripSerializer(strip, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Process"],
    summary="Get or update process section",
    description="Manage process section content."
)
@method_decorator(csrf_exempt, name='dispatch')
class ProcessSectionView(APIView):
    """Process section management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        section, created = ProcessSection.objects.get_or_create(is_active=True)
        serializer = ProcessSectionSerializer(section)
        return Response(serializer.data)
    
    def put(self, request):
        section, created = ProcessSection.objects.get_or_create(is_active=True)
        serializer = ProcessSectionSerializer(section, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - ORR Report"],
    summary="Get or update ORR report section",
    description="Manage ORR report section content."
)
@method_decorator(csrf_exempt, name='dispatch')
class ORRReportSectionView(APIView):
    """ORR report section management"""
    
    def get_permissions(self):
        return []
    
    def get(self, request):
        section, created = ORRReportSection.objects.get_or_create(is_active=True)
        serializer = ORRReportSectionSerializer(section)
        return Response(serializer.data)
    
    def put(self, request):
        section, created = ORRReportSection.objects.get_or_create(is_active=True)
        serializer = ORRReportSectionSerializer(section, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["CMS - Images"],
    summary="Upload image",
    description="Upload image file and return URL."
)
@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(APIView):
    """Image upload for CMS"""
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def post(self, request):
        try:
            if 'image' not in request.FILES:
                return Response(
                    {'error': 'No image file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image_file = request.FILES['image']
            
            # Validate file size (max 10MB)
            if image_file.size > 10 * 1024 * 1024:
                return Response(
                    {'error': 'File size too large. Maximum 10MB allowed.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if image_file.content_type not in allowed_types:
                return Response(
                    {'error': 'Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate unique filename
            file_extension = os.path.splitext(image_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Save file
            file_path = f"business_systems/{unique_filename}"
            saved_path = default_storage.save(file_path, ContentFile(image_file.read()))
            
            # Return URL
            image_url = f"/media/{saved_path}"
            
            return Response({
                'success': True,
                'status': 200,
                'message': 'Image uploaded successfully',
                'data': {
                    'image_url': image_url,
                    'filename': unique_filename,
                    'file_path': saved_path
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Upload failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["CMS - All Content"],
    summary="Get all homepage content",
    description="Fetch all homepage content in a single request for better performance."
)
class AllHomepageContentView(APIView):
    """Get all homepage content at once"""
    
    def get(self, request):
        try:
            # Get or create all content sections
            homepage, _ = HomePage.objects.get_or_create(is_active=True)
            approach_section, _ = ApproachSection.objects.get_or_create(is_active=True)
            business_system_section, _ = BusinessSystemSection.objects.get_or_create(is_active=True)
            orr_role_section, _ = ORRRoleSection.objects.get_or_create(is_active=True)
            message_strip, _ = MessageStrip.objects.get_or_create(is_active=True)
            process_section, _ = ProcessSection.objects.get_or_create(is_active=True)
            orr_report_section, _ = ORRReportSection.objects.get_or_create(is_active=True)
            contact_info, _ = ContactInfo.objects.get_or_create(is_active=True)
            
            # Get lists
            service_cards = ServiceCard.objects.filter(is_active=True).order_by('order')
            faqs = FAQ.objects.filter(is_active=True).order_by('category', 'order')
            testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
            
            # Serialize all data
            data = {
                'homepage': HomePageSerializer(homepage).data,
                'approach_section': ApproachSectionSerializer(approach_section).data,
                'business_system_section': BusinessSystemSectionSerializer(business_system_section).data,
                'orr_role_section': ORRRoleSectionSerializer(orr_role_section).data,
                'message_strip': MessageStripSerializer(message_strip).data,
                'process_section': ProcessSectionSerializer(process_section).data,
                'orr_report_section': ORRReportSectionSerializer(orr_report_section).data,
                'contact_info': ContactInfoSerializer(contact_info).data,
                'service_cards': ServiceCardSerializer(service_cards, many=True).data,
                'faqs': FAQSerializer(faqs, many=True).data,
                'testimonials': TestimonialSerializer(testimonials, many=True).data,
            }
            
            return Response({
                'success': True,
                'status': 200,
                'message': 'All content fetched successfully',
                'data': data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'status': 500,
                'message': f'Error fetching content: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)