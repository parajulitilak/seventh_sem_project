"""
URL configuration for summarizer_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# summarizer_project/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from summarizer_app.views import homepage,front_page

urlpatterns = [
    path('', front_page, name='front_page'),
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('', include('summarizer_app.urls')),
    path('summarization/', include('summarizer_app.urls')),## do not remove this this is for summarization url
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)