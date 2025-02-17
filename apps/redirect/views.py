from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.url_management.models import RedirectRule


class PublicRedirectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, redirect_identifier):
        rule = get_object_or_404(RedirectRule, redirect_identifier=redirect_identifier, is_private=False)
        return redirect(rule.redirect_url)


class PrivateRedirectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, redirect_identifier):
        print("Request user:", request.user)
        print("Redirect Identifier:", redirect_identifier)

        rule = get_object_or_404(RedirectRule, redirect_identifier=redirect_identifier, is_private=True,
                                 owner=request.user)
        print(rule.redirect_url)
        return redirect(rule.redirect_url)
