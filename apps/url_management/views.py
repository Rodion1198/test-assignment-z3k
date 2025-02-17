from rest_framework import viewsets, permissions
from .models import RedirectRule
from .serializers import RedirectRuleSerializer
from .permissions import IsOwnerPermission


class RedirectRuleViewSet(viewsets.ModelViewSet):
    serializer_class = RedirectRuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return RedirectRule.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
