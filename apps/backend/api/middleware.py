import re
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings


class CSRFExemptMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that exempts API endpoints from CSRF validation
    """
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Get exempt URLs from settings
        exempt_urls = getattr(settings, 'CSRF_EXEMPT_URLS', [])
        
        # Check if the current path matches any exempt URL pattern
        for pattern in exempt_urls:
            if re.match(pattern, request.path):
                # Mark the view as CSRF exempt
                setattr(callback, 'csrf_exempt', True)
                return None
        
        # Use default CSRF processing for non-exempt URLs
        return super().process_view(request, callback, callback_args, callback_kwargs)