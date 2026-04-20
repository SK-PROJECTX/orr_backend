from django.utils import translation
from django.conf import settings

class QueryParameterLocaleMiddleware:
    """
    Middleware that sets the language based on a 'lang' query parameter.
    This is useful for API requests from frontends that manage language state.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.GET.get('lang')
        
        # Check if language is supported
        supported_languages = [lang[0] for lang in settings.LANGUAGES]
        
        if language and language in supported_languages:
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
            print(f"DEBUG: Language activated from query parameter: {language}")
        else:
            print(f"DEBUG: Language not changed (lang={language}, supported={supported_languages})")
        
        response = self.get_response(request)
        
        # Deactivate translation after request
        translation.deactivate()
        
        return response
