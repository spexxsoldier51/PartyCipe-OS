"""project URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from welcome.views import index, health
from partycipe.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', index, name='home'),
    path('health/', health),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('partycipe/', Home),
    path('partycipe/party/join', JoinParty),
    path('partycipe/party/partipate', JoinParty),
    path('partycipe/party/create', create_party),
    path('partycipe/party/<int:id>', party_detail, name='party_detail'),
    path('partycipe/participate/change/<int:id>', ChangeParticipate, name="ChangeParticipate"),
    re_path(r'partycipe/party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))$', party_status, name='party-status'),
    re_path(r'partycipe/party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))\/join$', party_join, name='party-join'),
    re_path(r'partycipe/party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))\/mail$', send_mail, name='send_mail'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
