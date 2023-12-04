"""
URL configuration for property project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('base', views.BASE, name='base'),
    path('', views.HOME, name='home'),
    # Property
    path('property/', views.PROP, name='property'),
    path('property/<slug:slug>', views.PROP_DETAIL, name='property_detail'),
    path('property/<str:category>/', views.PROP_CATEGORY, name='property_category'),
    path('latest/', views.PROP_LATEST, name='latest'),
    path('popular/', views.PROP_POPULAR, name='popular'),
    path('category/<str:category>/', views.CAT_DETAIL, name='category'),

    # Gallery
    path('gallery/', views.GALLERY, name='gallery'),
    path('search/', views.PROP_SEARCH, name='search_results'),
    # Contact Us
    path('contact/', views.CONTACT, name='contact')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 
