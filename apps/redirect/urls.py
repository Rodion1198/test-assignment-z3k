from django.urls import path
from .views import PublicRedirectView, PrivateRedirectView

urlpatterns = [
    path('redirect/public/<str:redirect_identifier>/', PublicRedirectView.as_view(), name='public-redirect'),
    path('redirect/private/<str:redirect_identifier>/', PrivateRedirectView.as_view(), name='private-redirect'),
]
