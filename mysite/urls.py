"""mysite URL Configuration

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
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from polls import views
from polls.forms import LoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('polls/login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='polls/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('polls/logout/', auth_views.LogoutView.as_view(template_name='polls/logout.html'), name='logout'),
    path('polls/password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('polls/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='polls/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('polls/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='polls/password_reset_complete.html'),
         name='password_reset_complete'),
    path('polls/password-change/', views.ChangePasswordView.as_view(), name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
