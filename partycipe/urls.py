from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('', Home),

    path('party/join', JoinParty),
    path('party/partipate', JoinParty),
    path('party/create', create_party),
    path('party/<int:id>', party_detail, name='party_detail'),



    path('participate/change/<int:id>', ChangeParticipate, name="ChangeParticipate"),

    re_path(r'party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))$', party_status, name='party-status'),
    re_path(r'party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))\/join$', party_join, name='party-join'),

    re_path(r'party\/(?P<signed_pk>(?:[0-9]+\/[A-Za-z0-9_=-]+))\/mail$', send_mail, name='send_mail'),


]

urlpatterns += staticfiles_urlpatterns()