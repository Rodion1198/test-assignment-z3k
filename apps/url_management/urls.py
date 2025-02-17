from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RedirectRuleViewSet

router = DefaultRouter()
router.register(r'url', RedirectRuleViewSet, basename='redirectrule')

urlpatterns = [
    path('', include(router.urls)),
]
