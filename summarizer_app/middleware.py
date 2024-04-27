# summarizer_app/middleware.py
from django.http import HttpResponseRedirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse('summarizer_app:login') and request.path != reverse('summarizer_app:register') and request.path != reverse('summarizer_app:front_page'):
            return HttpResponseRedirect(reverse('summarizer_app:front_page'))
        return self.get_response(request)
