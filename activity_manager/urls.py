"""activity_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('famille/', include('famille.urls')),
    path('activite/', include('activite.urls')),
    path('user/', include('user.urls')),
    path('pointage/', include('pointage.urls')),
    re_path(r'^comptabilite/', include('comptabilite.urls')),
    path('login/',views.LoginView.as_view(template_name='login.html')),
    path('logout',views.LogoutView.as_view()),
    path('changepassword/',views.PasswordChangeView.as_view(template_name='changePassword.html')),
    path('resetpassword',views.PasswordResetView.as_view(template_name='resetPassword.html', success_url='user/')),
    path('password_change_done',views.PasswordChangeDoneView.as_view(template_name='resetPassword.html'), name='password_change_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    re_path(r'\w*', include('user.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
