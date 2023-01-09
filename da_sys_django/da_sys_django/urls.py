"""da_sys_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

# using django built-in login
from django.contrib.auth import views
from da_sys_django.form import UserLoginForm
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
urlpatterns += [
    path('login/',
         views.LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=UserLoginForm),
         name='login'
         )]
urlpatterns += [
    path('logout/',
         views.LogoutView.as_view(
             template_name='registration/logout.html'),
         name='logout'
         )]

# with django allauth
urlpatterns += [
    path('allauth/', include('allauth.urls')),  # django-allauth網址
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# add app urls
urlpatterns += [
    path('recommender/', include('recommender.urls')),
]

# Add URL maps to redirect the base URL to our selected application
from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/recommender/', permanent=True)),
]
