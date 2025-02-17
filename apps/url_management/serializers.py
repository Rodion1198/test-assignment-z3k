from rest_framework import serializers
from .models import RedirectRule


class RedirectRuleSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RedirectRule
        fields = ['id', 'created', 'modified', 'owner', 'redirect_url', 'is_private', 'redirect_identifier']
        read_only_fields = ['id', 'created', 'modified', 'redirect_identifier']
