from rest_framework import serializers

from call_applications.models import CallForApplication


class CallForApplicationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CallForApplication
        exclude = ('updated_on', 'created_on')
        read_only_fields = ('id',)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)